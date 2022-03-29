
import binascii
import os
from django.db import models
from django.contrib.auth.models import AbstractUser
class User(AbstractUser):
   """Abstract the base user of django user model and create the API User of it"""
   email = models.EmailField(max_length=150, unique=True)
   phone_number = models.CharField(max_length=20,unique=True)
   dob = models.DateField()
   street = models.CharField(max_length=100)
   zip_code = models.IntegerField()
   city = models.CharField(max_length=100)
   state = models.CharField(max_length=100)
   country = models.CharField(max_length=50) 
   password= models.CharField(max_length=200)

   def __str__(self):
      """Return the user with its email address name"""
      return self.email


