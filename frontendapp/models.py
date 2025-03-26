
# Create your models here.
from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

from django.contrib.auth.models import AbstractUser, Group, Permission
from django.db import models

class CustomUser(AbstractUser):
    email = models.EmailField(unique=True)  # Ensure email is unique
    user_role = models.CharField(max_length=50, choices=[
        ('donor', 'Donor'),
        ('beneficiary', 'Beneficiary'),
        ('blood_donor', 'Blood Donor'),
        ('employee', 'Employee'),
    ], default='donor')

    groups = models.ManyToManyField(Group, related_name="customuser_groups", blank=True)
    user_permissions = models.ManyToManyField(Permission, related_name="customuser_permissions", blank=True)

    USERNAME_FIELD = "email"  # Use email instead of username
    REQUIRED_FIELDS = []  # No additional required fields

    def __str__(self):
        return self.email  # Show email instead of username

from django.conf import settings
from django.db import models

from django.db import models
from django.conf import settings

class Donation(models.Model):
    donor = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="donations")
    amount = models.DecimalField(max_digits=10, decimal_places=2)
    donation_type = models.CharField(max_length=50, choices=[
        ('Money', 'Money'),
        ('Clothes', 'Clothes'),
        ('Food', 'Food'),
        ('Medical Supplies', 'Medical Supplies')
    ])  # ✅ Ensure this field exists
    date = models.DateTimeField(auto_now_add=True)
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved')])
    

    def __str__(self):
        return f"{self.donor.username} - {self.amount} - {self.donation_type}"

from rest_framework import serializers
from .models import Donation

class DonationSerializer(serializers.ModelSerializer):
    class Meta:
        model = Donation
        fields = '__all__'
from django.db import models
from django.conf import settings

class BeneficiaryRequest(models.Model):
    beneficiary = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name="requests")
    service_type = models.CharField(max_length=100, choices=[
        ('Education Support', 'Education Support'),
        ('Medical Treatment', 'Medical Treatment'),
        ('Old Age Home Support', 'Old Age Home Support'),
    ])
    request_date = models.DateTimeField(auto_now_add=True)
    status = models.CharField(max_length=20, choices=[('Pending', 'Pending'), ('Approved', 'Approved'), ('Rejected', 'Rejected')], default='Pending')
    receipt = models.FileField(upload_to='receipts/', null=True, blank=True)

    def __str__(self):
        return f"{self.beneficiary.username} - {self.service_type} - {self.status}"

from django.db import models
class signupdb(models.Model):


    username = models.CharField(max_length=100, unique=True)
    email = models.EmailField(unique=True)
    password = models.CharField(max_length=255)
    cpassword=models.CharField(max_length=100)

    def __str__(self):
        return self.username

from django.db import models

import uuid
from django.db import models

class payment_donation(models.Model):
    username = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    amount = models.IntegerField(null=True)
    transaction_id = models.CharField(max_length=100, unique=True, blank=True)  # Allow blank initially
    payment_date = models.DateTimeField(auto_now_add=True)

    def save(self, *args, **kwargs):
        if not self.transaction_id or self.transaction_id == "00":  # Prevent incorrect saving
            short_category = "".join([word[:2] for word in self.category.split()])[:4]
            unique_id = uuid.uuid4().hex[:4]
            self.transaction_id = f"{short_category}{unique_id}".upper()
            print(f"Generated Transaction ID: {self.transaction_id}")  # Debugging print

        super().save(*args, **kwargs)
    def __str__(self):
        return f"{self.username} donated ${self.amount} to {self.category} (Txn: {self.transaction_id})"


from django.conf import settings
from django.db import models

class UserProfile(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    profile_picture = models.ImageField(upload_to='profile_pics/', default='default.jpg')
    full_name = models.CharField(max_length=255)
    email = models.EmailField()
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    address = models.TextField(blank=True, null=True)

    def __str__(self):
        return self.user.username
from django.db import models
from django.utils.timezone import now

class ServiceRequest(models.Model):
    STATUS_CHOICES = [
        ("Pending", "Pending"),
        ("Approved", "Approved"),
        ("Rejected", "Rejected"),
    ]

    username = models.CharField(max_length=255)
    category = models.CharField(max_length=255)
    request_date = models.DateTimeField(default=now)
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default="Pending")

    def __str__(self):
        return f"{self.username} requested {self.category} on {self.request_date.strftime('%Y-%m-%d')} - {self.status}"



from django.db import models

class blood_module(models.Model):
    BLOOD_GROUPS = [
        ('A+', 'A+'), ('A-', 'A-'),
        ('B+', 'B+'), ('B-', 'B-'),
        ('O+', 'O+'), ('O-', 'O-'),
        ('AB+', 'AB+'), ('AB-', 'AB-'),
    ]

    AVAILABILITY_CHOICES = [
        ('Yes', 'Yes'),
        ('No', 'No'),
    ]

    full_name = models.CharField(max_length=100)
    blood_group = models.CharField(max_length=3, choices=BLOOD_GROUPS)
    mobile = models.IntegerField(unique=True)
    location = models.CharField(max_length=100)
    availability = models.CharField(max_length=3, choices=AVAILABILITY_CHOICES)
    registered_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.full_name} ({self.blood_group})"

