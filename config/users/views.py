from django.shortcuts import render, redirect
from django.contrib import messages
from django.http import JsonResponse
from .models import User, Mechanic, ContactMessage
from django.views.decorators.csrf import csrf_exempt
from google.oauth2 import id_token
from google.auth.transport import requests as google_requests
import json
import requests
import random
from django.conf import settings


def landing(request):
    if request.method == "POST":
        name = request.POST.get('name')
        mobile_number = request.POST.get('mobile_number')
        subject = request.POST.get('subject')
        message = request.POST.get('message')
        

        if name and mobile_number and message:
            ContactMessage.objects.create(
                name=name,
                mobile_number=mobile_number,
                subject=subject,
                message=message
            )
            messages.success(request, "Your message has been sent successfully! We will get back to you shortly.")
            return redirect('/#contact')
            
    return render(request, 'MechalocateLanding.html')


def check_mobile(request):
    mobile = request.GET.get('mobile', '').strip()
    user_type = request.GET.get('type', 'user')
    
    if user_type == 'pro':
        exists = Mechanic.objects.filter(mobile_number=mobile).exists()
    else:
        exists = User.objects.filter(mobilenumber=mobile).exists()
        
    return JsonResponse({'exists': exists})


def centre(request):
    return render(request, 'UserCentre.html')


def register(request):
    if request.method == "POST":
        firstname = request.POST.get('firstname')
        lastname = request.POST.get('lastname')
        mobilenumber = request.POST.get('mobilenumber')
        email = request.POST.get('email')
        password = request.POST.get('password')

        licenses = request.FILES.get('licenses')
        llr = request.FILES.get('llr')
        insurance = request.FILES.get('insurance')
        rc = request.FILES.get('rc')

        User.objects.create(
            firstname=firstname,
            lastname=lastname,
            mobilenumber=mobilenumber,
            email=email,
            password=password,
            licenses=licenses,
            llr=llr,
            insurance=insurance,
            rc=rc
        )

        return redirect('login')

    return render(request, 'UserReg.html')


def login(request):
    if request.method == "POST":
        email = request.POST.get("email", "").strip()
        password = request.POST.get("password", "")

        user = User.objects.filter(email=email, password=password).first()
        if user:
            request.session['user_id'] = user.id
            return render(request, "UserLog.html", {"login_success": True})

        return render(
            request,
            "UserLog.html",
            {
                "login_error": "Invalid email or password.",
                "entered_email": email,
            },
        )

    return render(request, 'UserLog.html')


def dashboard(request):
    user_id = request.session.get('user_id')
    user = User.objects.filter(id=user_id).first() if user_id else None
    return render(request, 'UserDash.html', {'user': user})


def pro_centre(request):
    return render(request, 'ProCentre.html')


def pro_log(request):
    return render(request, 'ProLog.html')


def pro_dash(request):
    active_requests = ContactMessage.objects.all().order_by('-created_at')
    return render(request, 'Prodash.html', {'active_requests': active_requests})


def pro_reg(request):
    if request.method == "POST":
        full_name = request.POST.get('full_name', '').strip()
        mobile_number = request.POST.get('mobile_number', '').strip()
        service_type = request.POST.get('service_type', '').strip()
        mechanic_type = request.POST.get('mechanic_type', '').strip()
        years_of_experience = request.POST.get('years_of_experience', '0').strip()
        location = request.POST.get('location', '').strip()

        Mechanic.objects.create(
            full_name=full_name,
            mobile_number=mobile_number,
            service_type=service_type,
            mechanic_type=mechanic_type,
            years_of_experience=int(years_of_experience),
            location=location,
        )

        return redirect('pro_log')

    return render(request, 'ProReg.html')

import requests
import random
from django.conf import settings

def send_otp(request):
    mobile = request.GET.get('mobile', '').strip()
    if not mobile:
        return JsonResponse({'success': False, 'message': 'Mobile number missing'})

    otp_code = str(random.randint(1000, 9999))
    request.session[f'temp_otp_{mobile}'] = otp_code
    
    url = "https://www.fast2sms.com/dev/bulkV2"
    params = {
        "authorization": settings.FAST2SMS_API_KEY,
        "variables_values": otp_code,
        "route": "otp",
        "numbers": mobile
    }
    
    try:
        response = requests.get(url, params=params)
        response_data = response.json()
        if response_data.get('return'):
            return JsonResponse({'success': True, 'message': 'OTP sent successfully'})
        else:
            return JsonResponse({'success': False, 'message': response_data.get('message', 'Failed to send OTP')})
    except Exception as e:
        return JsonResponse({'success': False, 'message': str(e)})

def verify_otp(request):
    mobile = request.GET.get('mobile', '').strip()
    otp = request.GET.get('otp', '').strip()
    
    if not mobile or not otp:
        return JsonResponse({'success': False, 'message': 'Mobile and OTP are required'})
        
    session_otp = request.session.get(f'temp_otp_{mobile}')
    
    if session_otp and session_otp == otp:
        del request.session[f'temp_otp_{mobile}']
        return JsonResponse({'success': True})
    else:
        return JsonResponse({'success': False, 'message': 'Invalid OTP'})

@csrf_exempt
def google_sso_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get('credential')
            
            if not token:
                return JsonResponse({'success': False, 'message': 'No credential provided'})

            # Verify the token
            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                '1088181726401-9entbbkjdv9q4eonlmrnl9q4h6j6jpcr.apps.googleusercontent.com'
            )
            
            # Extract info
            email = idinfo.get('email')
            firstname = idinfo.get('given_name', '')
            lastname = idinfo.get('family_name', '')
            action = data.get('action', 'login')
            
            if not email:
                return JsonResponse({'success': False, 'message': 'No email provided by Google'})
                
            if action == 'login':
                user = User.objects.filter(email=email).first()
                if not user:
                    return JsonResponse({'success': False, 'message': 'Account not found. Please register first.'})
                request.session['user_id'] = user.id
            else:
                user, created = User.objects.get_or_create(
                    email=email,
                    defaults={
                        'firstname': firstname,
                        'lastname': lastname,
                        'password': 'google_sso_no_password',
                        'mobilenumber': ''
                    }
                )
                request.session['user_id'] = user.id
            
            return JsonResponse({'success': True, 'redirect_url': '/dashboard/'})
            
        except ValueError as e:
            return JsonResponse({'success': False, 'message': f'Invalid token: {str(e)}'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def google_sso_pro_login(request):
    if request.method == "POST":
        try:
            data = json.loads(request.body)
            token = data.get('credential')
            
            if not token:
                return JsonResponse({'success': False, 'message': 'No credential provided'})

            idinfo = id_token.verify_oauth2_token(
                token, 
                google_requests.Request(), 
                '1088181726401-9entbbkjdv9q4eonlmrnl9q4h6j6jpcr.apps.googleusercontent.com'
            )
            
            email = idinfo.get('email')
            firstname = idinfo.get('given_name', '')
            lastname = idinfo.get('family_name', '')
            action = data.get('action', 'login')
            
            if not email:
                return JsonResponse({'success': False, 'message': 'No email provided by Google'})
                
            if action == 'login':
                if not Mechanic.objects.filter(email=email).exists():
                    return JsonResponse({'success': False, 'message': 'Account not found. Please register first.'})
            else:
                mechanic, created = Mechanic.objects.get_or_create(
                    email=email,
                    defaults={
                        'full_name': f"{firstname} {lastname}".strip(),
                        'mobile_number': '',
                        'service_type': 'mechanic',
                        'mechanic_type': 'two',
                        'years_of_experience': 0,
                        'location': ''
                    }
                )
            
            return JsonResponse({'success': True, 'redirect_url': '/prodash/'})
            
        except ValueError as e:
            return JsonResponse({'success': False, 'message': f'Invalid token: {str(e)}'})
        except Exception as e:
            return JsonResponse({'success': False, 'message': str(e)})
            
    return JsonResponse({'success': False, 'message': 'Invalid request method'})

@csrf_exempt
def save_user_docs(request):
    if request.method == "POST":
        user_id = request.session.get('user_id')
        if not user_id:
            return JsonResponse({'success': False, 'message': 'User not logged in'})
        
        user = User.objects.filter(id=user_id).first()
        if not user:
            return JsonResponse({'success': False, 'message': 'User not found'})
            
        if 'licenses' in request.FILES:
            user.licenses = request.FILES['licenses']
        if 'llr' in request.FILES:
            user.llr = request.FILES['llr']
        if 'insurance' in request.FILES:
            user.insurance = request.FILES['insurance']
        if 'rc' in request.FILES:
            user.rc = request.FILES['rc']
            
        user.save()
        
        return JsonResponse({'success': True, 'message': 'Documents saved successfully'})
    return JsonResponse({'success': False, 'message': 'Invalid request method'})