from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField

from utils.constants import ROLES


class MyUserManager(UserManager):
    use_in_migrations = True

    def _create_user(self, email, password, role, phone, first_name, last_name, pincode, **extra_fields):
        """Create and save a User with the given email and password."""
        if not email:
            raise ValueError('The given email must be set')
        email = self.normalize_email(email)
        user = self.model(
            email=email, 
            role=role,
            phone=phone,
            first_name=first_name,
            last_name=last_name,
            pincode=pincode,
            **extra_fields
            )
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_user(self, email, password, role, phone, first_name, last_name, pincode, **extra_fields):
        """Create and save a regular User with the given email and password."""
        extra_fields.setdefault('is_staff', False)
        extra_fields.setdefault('is_superuser', False)
        return self._create_user(email, password, role, phone, first_name, last_name, pincode, **extra_fields)

    def create_superuser(self, email, password, role, phone, first_name, last_name, pincode, **extra_fields):
        """Create and save a SuperUser with the given email and password."""
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self._create_user(email, password, role, phone, first_name, last_name, pincode, **extra_fields)

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    username = None
    email = models.EmailField(unique=True)
    role = models.CharField(max_length=8, choices=[(e.value, e.value) for e in ROLES])
    phone = PhoneNumberField(null=False, blank=False)

    first_name = models.CharField(max_length=254)
    last_name = models.CharField(max_length=254)

    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    pincode = models.DecimalField(max_digits=6, decimal_places=0) # TODO exact 6 digit

    # TODO password constraints
    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['role', 'phone', 'first_name', 'last_name', 'pincode']
    
    objects = MyUserManager()

    def __str__(self):
       return self.email
    
    class Meta:
        ordering = ['email']