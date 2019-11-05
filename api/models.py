
import datetime
import uuid

from django.contrib.auth.base_user import AbstractBaseUser, BaseUserManager
from django.contrib.auth.models import PermissionsMixin
from django.db import models
from django.utils import timezone


class UserManager(BaseUserManager):
    
    def collect_list_users(self, check_point, limit, *args, **kwargs):
        return User.objects.filter(created_at__lte=check_point).order_by('-created_at')[:limit]

class User(AbstractBaseUser, PermissionsMixin):
    GENDER_CHOICES = (
        ('1', 'MALE'),
        ('2', 'FEMALE'),
        ('3', 'OTHERS'),
        )
    uid = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    email = models.EmailField(unique=True, db_index=True, null=True, editable=False)
    fb_id = models.CharField(unique=True, max_length=255, db_index=True, null=True, editable=False)
    password = models.CharField(max_length=20, null=False)
    account_type = models.IntegerField(null=False, editable=False) #0: Email, 1: Face
    fullname = models.CharField(max_length=255, null=True)
    gender = models.BooleanField(choices=GENDER_CHOICES, max_length=1, null=True)
    birthday = models.DateField(null=True)
    avatar = models.CharField(max_length=255, null=True)
    is_banned = models.BooleanField(default=False, null=False)
    created_at = models.DateTimeField(default=timezone.now(), null=False)
    is_activated = models.BooleanField(default=False, null=False)

    objects = UserManager()
    
    def save(self, *args, **kwargs):
        self.account_type = 1 if(self.fb_id) else 0
        super().save(*args, **kwargs)


    USERNAME_FIELD = 'uid'

    class Meta:
        ordering = ['created_at']
    
    # def __str__(self):
    #     return self.email

class UserOTP(models.Model):
    uid = models.CharField(primary_key=True, max_length=255, editable=False)
    email = models.EmailField(unique=True, null=False, blank=False)
    otp_code_reset_pass = models.CharField(max_length=10)

    objects = models.Manager()