import uuid
import pytz
from django.contrib.auth.base_user import BaseUserManager
from django.contrib.auth.models import AbstractUser
from django.db import models
from django.utils.translation import ugettext_lazy as _
from .utils import get_username
# Create your models here.


class UserManager(BaseUserManager):

    def create_user(self, username, password, email=None, role=None):
        if not role:
            role = User.UNDEFINED
        email = self.normalize_email(email)
        user = self.model(username=username,
                          email=email,

                          role=role)
        user.set_password(password)
        user.save()
        return user

    def create_superuser(self, username, password, email=None, role=None):
        role = User.SUPER_USER
        user = self.create_user(username, password, email,  role)
        user.is_staff = True
        user.is_superuser = True
        user.save()
        return user


class User(AbstractUser):
    """
    Custom User has fields First Name, Last Name, Email Address
     and Role in the website
    """
    class Meta:
        verbose_name_plural = _("Users")

    id = models.UUIDField(
        primary_key=True,
        default=uuid.uuid4,
        editable=False)
    email = models.EmailField(
        _('Email Address'), unique=True, null=True, blank=True)
    email_verified = models.BooleanField(default=False)
    SUPER_USER = 'SU'
    STUDENT = 'ST'
    TEACHER = 'TE'
    UNDEFINED = 'UD'
    ROLE_CHOICES = [
        (SUPER_USER, 'Super User'),
        (STUDENT, 'Student'),
        (TEACHER, 'Teacher'),
    ]
    role = models.CharField(
        max_length=2, choices=ROLE_CHOICES, default=UNDEFINED,)
    user_display_name = models.CharField(max_length=255, null=True, blank=True)

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['username']

    def __str__(self):
        return self.user_display_name

    def save(self, *args, **kwargs):
        if self.role != self.SUPER_USER and self.role != self.UNDEFINED:
            self.username = get_username(self)
        self.user_display_name = user_display(self)
        super(User, self).save(*args, **kwargs)


def user_display(user):
    """
    The way a user's name is displayed.
    Standard format is 'First-Name Last-Name' or if no Last-Name,
    'First-Name'. In case of Name not provided,
    returns 'Username'
    """
    firstname = user.first_name
    space = " " if user.last_name else ""
    lastname = user.last_name
    name = f'{firstname}{space}{lastname}' if firstname else user.username
    return name
