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

    address = models.TextField(null=True, blank=True)
    city = models.CharField(max_length=32, null=True, blank=True)
    state = models.CharField(max_length=32, null=True, blank=True)
    country = models.CharField(max_length=32, null=True, blank=True)
    pincode = models.DecimalField(max_digits=6, decimal_places=0) # TODO exact 6 digit

    # TODO password constraints
    # TODO replace username with email
    # TODO first_name and last_name compulsary
    
    objects = MyUserManager()

    def __str__(self):
       return self.email