"""
Database Models
"""

from django.conf import settings
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from djongo import models as mongo_models


class UserManager(BaseUserManager):
    """Manager for user."""

    def create_user(self, email, password=None, **extra_fields):
        """Create, save and return new user"""
        if not email:
            raise ValueError('User must have an email address.')
        user = self.model(email=self.normalize_email(email), **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, email, password):
        """Create and return new superuser"""
        user = self.create_user(email, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """User in the system."""
    class Meta:
        ordering = ['id']

    email = models.EmailField(max_length=255, unique=True)
    first_name = models.CharField(max_length=255)
    last_name = models.CharField(max_length=255)
    address = models.CharField(max_length=255)
    bio = models.CharField(max_length=255)
    occupation = models.CharField(max_length=255)
    expertise = models.CharField(max_length=255)
    is_active = models.BooleanField(default=True)
    is_mentor = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'


class Request(models.Model):
    """Mentorship Request Model"""
    class Meta:
        ordering = ['id']

    mentor = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='mentor',
       on_delete=models.CASCADE
    )
    mentee = models.ForeignKey(
       settings.AUTH_USER_MODEL,
       related_name='mentee',
       on_delete=models.CASCADE
    )
    question = models.CharField(max_length=255)
    status = models.CharField(max_length=255, default="Pending")

    def __str__(self) -> str:
        """To string method"""
        return self.question


class Log(mongo_models.Model):
    _id = mongo_models.ObjectIdField()
    message = mongo_models.TextField(max_length=1000)

    created_at = mongo_models.DateTimeField(auto_now_add=True)
    updated_at = mongo_models.DateTimeField(auto_now=True)

    class Meta:
        _use_db = 'nonrel'
        ordering = ("-created_at", )

    def __str__(self):
        return self.message
