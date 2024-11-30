
''' Database models '''
from django.db import models
from django.contrib.auth.models import (
    AbstractBaseUser, BaseUserManager, PermissionsMixin
)


class UserManager(BaseUserManager):
    """" The Base user manager """
    def create_user(self, email, password, phone_number, **extra_fields):
        """ Create the user and return """
        if not email:
            raise ValueError('New User Must Have a valid Email Address')
        if email is None:
            raise ValueError('Email cannot be None')
        if not phone_number:
            raise ValueError('A valid phone number is needed')
        user = self.model(email=self.normalize_email(email),
                          phone_number=phone_number, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user


class User(AbstractBaseUser, PermissionsMixin):
    """ User in the system """
    email = models.EmailField(max_length=255, unique=True)
    name = models.CharField(max_length=255)
    phone_number = models.CharField(max_length=15, unique=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)

    objects = UserManager()

    USERNAME_FIELD = 'email'
