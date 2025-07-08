from django.db import models
from django.contrib.auth.hashers import make_password, check_password
import secrets
from datetime import datetime, timedelta
from django.utils import timezone

# Create your models here.

class User(models.Model):
    # basic details of the user
    username = models.CharField(max_length=150, unique=True)
    password = models.CharField(max_length=128)  # Store hashed passwords
    first_name = models.CharField(max_length=30, blank=True)
    last_name = models.CharField(max_length=30, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    # email data of the user
    email = models.EmailField(unique=True)
    email_verified = models.BooleanField(default=False)
    email_verification_token = models.CharField(max_length=64, blank=True, null=True)
    email_verification_token_created_at = models.DateTimeField(blank=True, null=True)
    email_verified_at = models.DateTimeField(blank=True, null=True)

    # phone data of the user
    phone_number = models.CharField(max_length=15, blank=True, null=True)
    phone_verified = models.BooleanField(default=False)
    phone_verification_token = models.CharField(max_length=6, blank=True, null=True)  # 6 digit OTP
    phone_verification_token_created_at = models.DateTimeField(blank=True, null=True)
    phone_verified_at = models.DateTimeField(blank=True, null=True)
    
    # Rate limiting for OTP resend
    otp_resend_count = models.IntegerField(default=0)
    last_otp_resend = models.DateTimeField(blank=True, null=True)

    # update
    is_verified = models.BooleanField(default=False)
    is_active = models.BooleanField(default=True)
    updated_at = models.DateTimeField(auto_now=True)

    #device info at the time of creation
    device_info = models.JSONField(blank=True, null=True)

    def set_password(self, raw_password):
        self.password = make_password(raw_password)

    def check_password(self, raw_password):
        return check_password(raw_password, self.password)

    def generate_phone_otp(self):
        """Generate 6 digit OTP for phone verification"""
        self.phone_verification_token = str(secrets.randbelow(1000000)).zfill(6)
        self.phone_verification_token_created_at = timezone.now()
        self.save()
        return self.phone_verification_token

    def is_otp_valid(self):
        """Check if OTP is still valid (5 minutes)"""
        if not self.phone_verification_token_created_at:
            return False
        return timezone.now() - self.phone_verification_token_created_at < timedelta(minutes=5)

    def can_resend_otp(self):
        """Check if user can resend OTP (rate limiting)"""
        now = timezone.now()
        
        # Reset count if 24 hours have passed
        if self.last_otp_resend and (now - self.last_otp_resend).total_seconds() > 86400:  # 24 hours
            self.otp_resend_count = 0
            self.save()
        
        # Allow max 5 resends per day
        if self.otp_resend_count >= 5:
            return False, "Maximum OTP resend limit reached for today"
        
        # Must wait 1 minute between resends
        if self.last_otp_resend and (now - self.last_otp_resend).total_seconds() < 60:
            remaining_time = 60 - int((now - self.last_otp_resend).total_seconds())
            return False, f"Please wait {remaining_time} seconds before requesting new OTP"
        
        return True, "OK"

    def resend_otp(self):
        """Resend OTP with rate limiting"""
        can_resend, message = self.can_resend_otp()
        if not can_resend:
            return None, message
        
        otp = self.generate_phone_otp()
        self.otp_resend_count += 1
        self.last_otp_resend = timezone.now()
        self.save()
        
        return otp, "OTP sent successfully"

    def verify_phone_otp(self, otp):
        """Verify phone OTP"""
        if self.phone_verification_token == otp and self.is_otp_valid():
            self.phone_verified = True
            self.phone_verified_at = timezone.now()
            self.is_verified = True
            self.phone_verification_token = None
            self.phone_verification_token_created_at = None
            # Reset resend count on successful verification
            self.otp_resend_count = 0
            self.last_otp_resend = None
            self.save()
            return True
        return False

    def __str__(self):
        return self.username

    class Meta:
        verbose_name = 'User'
        verbose_name_plural = 'Users'