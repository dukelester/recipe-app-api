
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

    def create_superuser(self, email, password, phone_number):
        """Create a superuser account.

        This method is responsible for creating a superuser with elevated
        privileges in the application. It ensures that the superuser
        has the necessary attributes
        and permissions to manage the application effectively.

        Args:
            self: The instance of the class.

        Returns:
            User: The created superuser instance.
        """
        user = self.create_user(email, password, phone_number)
        user.is_staff = True
        user.is_superuser = True
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
    REQUIRED_FIELDS = ['phone_number',]


class Recipe(models.Model):
    ''' The recipe model '''
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    description = models.TextField()
    time_in_minutes = models.IntegerField()
    price = models.DecimalField(decimal_places=2, max_digits=10)
    link = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self) -> str:
        return self.title
