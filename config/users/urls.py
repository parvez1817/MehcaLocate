from django.urls import path
from . import views

urlpatterns = [
    path('', views.landing, name='landing'),
    path('api/check-mobile/', views.check_mobile, name='check_mobile'),
    path('api/send-otp/', views.send_otp, name='send_otp'),
    path('api/verify-otp/', views.verify_otp, name='verify_otp'),
    path('api/google-login/', views.google_sso_login, name='google_sso_login'),
    path('api/google-pro-login/', views.google_sso_pro_login, name='google_sso_pro_login'),
    path('centre/', views.centre, name='centre'),
    path('register/', views.register, name='register'),
    path('login/', views.login, name='login'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('pro_centre/', views.pro_centre, name='pro_centre'),
    path('pro_log/', views.pro_log, name='pro_log'),
    path('prodash/', views.pro_dash, name='pro_dash'),
    path('pro_reg/', views.pro_reg, name='pro_reg'),
    path('api/update-docs/', views.save_user_docs, name='save_user_docs'),
]