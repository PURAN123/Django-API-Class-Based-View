from django.db import models
from django.contrib.auth.models import AbstractUser,Group
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
   school = models.ForeignKey('School', on_delete=models.CASCADE,blank=True,null=True)
   groups = models.ForeignKey(Group, on_delete=models.CASCADE,blank=True,null=True)

   def __str__(self):
      """Return the user with its email address name"""
      return self.email

class School(models.Model):
   name= models.CharField(max_length=100,unique=True)
   def __str__(self):
      return self.name
