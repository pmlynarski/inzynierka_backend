from django.contrib.auth.models import (AbstractBaseUser, BaseUserManager)
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver
from rest_framework.authtoken.models import Token

from grouper import settings


class UserManager(BaseUserManager):

    def create_user(self, first_name, last_name, email, is_staff=False, is_admin=False, is_active=True, password=None):
        if not email:
            raise ValueError("An email address is required")
        if not password:
            raise ValueError("A password is required")
        user_obj = self.model(
            email=self.normalize_email(email)
        )
        user_obj.set_password(password)
        user_obj.first_name = first_name
        user_obj.last_name = last_name
        user_obj.staff = is_staff
        user_obj.admin = is_admin
        user_obj.active = is_active
        user_obj.save()
        return user_obj

    def create_staff_user(self, first_name, last_name, email, password=None):
        user_obj = self.create_user(first_name=first_name, is_active=True, last_name=last_name, email=email,
                                    is_staff=True,
                                    password=password)
        return user_obj

    def create_superuser(self, first_name, last_name, email, password=None):
        user_obj = self.create_user(first_name=first_name, last_name=last_name, email=email, is_admin=True,
                                    is_staff=True, is_active=True, password=password)
        return user_obj


class User(AbstractBaseUser):
    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    active = models.BooleanField(default=True)
    admin = models.BooleanField(default=False)
    staff = models.BooleanField(default=False)
    lecturer = models.BooleanField(default=False)
    date_joined = models.DateTimeField(auto_now_add=True)
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['first_name', 'last_name']

    def __str__(self):
        return self.email

    def get_full_name(self):
        return self.first_name + ' ' + self.last_name

    def has_perm(self, perm, obj=None):
        return True

    def has_module_perms(self, app_label):
        return True

    @property
    def is_staff(self):
        return self.staff

    @property
    def is_admin(self):
        return self.admin

    @property
    def is_lecturer(self):
        return self.lecturer

    @property
    def is_active(self):
        return self.active

    objects = UserManager()


@receiver(post_save, sender=settings.AUTH_USER_MODEL)
def create_auth_token(sender, instance=None, created=False, **kwargs):
    if created:
        Token.objects.create(user=instance)
