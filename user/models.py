from django.db import models
import uuid
from django.contrib.auth.models import AbstractUser, UserManager
from phonenumber_field.modelfields import PhoneNumberField

from utils.constants import ROLES


class MyUserManager(UserManager):
    pass

class User(AbstractUser):
    user_id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)

    email = models.EmailField(unique=True)
    role = models.CharField(max_length=8, choices=[(e.value, e.value) for e in ROLES])
    phone = PhoneNumberField(null=False, blank=False)
    address = models.TextField()
    city = models.CharField(max_length=32, null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    pincode = models.DecimalField(max_digits=6, decimal_places=0, blank=True, null=True)

    # TODO password constrainsts
    # TODO replace username with email
    
    objects = MyUserManager()