from django.db import models


class User(models.Model):
    firstname = models.CharField(max_length=100)
    lastname = models.CharField(max_length=100)
    mobilenumber = models.CharField(max_length=100, default="")
    email = models.EmailField()
    password = models.CharField(max_length=100)

    licenses = models.ImageField(upload_to='documents/', null=True, blank=True)
    llr = models.ImageField(upload_to='documents/', null=True, blank=True)
    insurance = models.ImageField(upload_to='documents/', null=True, blank=True)
    rc = models.ImageField(upload_to='documents/', null=True, blank=True)

    def __str__(self):
        return self.firstname + " " + self.lastname


class Mechanic(models.Model):

    SERVICE_CHOICES = [
        ('mechanic', 'Mechanic'),
        ('tyre', 'Tyre Repairer'),
        ('both', 'Both'),
    ]

    MECHANIC_TYPE_CHOICES = [
        ('two', 'Two Wheeler'),
        ('four', 'Four Wheeler'),
        ('both', 'Both'),
    ]

    full_name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=15)
    email = models.EmailField(null=True, blank=True)
    service_type = models.CharField(max_length=20, choices=SERVICE_CHOICES)
    mechanic_type = models.CharField(max_length=20, choices=MECHANIC_TYPE_CHOICES)
    years_of_experience = models.PositiveIntegerField()
    location = models.CharField(max_length=255)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.get_service_type_display()})"

class ContactMessage(models.Model):
    name = models.CharField(max_length=200)
    mobile_number = models.CharField(max_length=15, default="")
    subject = models.CharField(max_length=255)
    message = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.name} - {self.subject}" 