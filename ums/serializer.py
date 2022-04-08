
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes
from django.utils.http import urlsafe_base64_encode
from rest_framework import serializers
from userms import settings

from .models import School, User
from .tokens import generate_token


class SchoolSerializer(serializers.ModelSerializer):
   """ School serializer for school model """
   class Meta:
      model= School
      fields= ['id','name',]


class GroupSerializer(serializers.ModelSerializer):
   """ Group serializer for group model """
   class Meta:
      model= Group
      fields=['id','name']


class UserListSerializer(serializers.ModelSerializer):
   """list a serializer to the model user """
   school= SchoolSerializer()
   groups= GroupSerializer()
   class Meta:
      model=  User
      fields= ["id", "username", "email", "phone_number", "dob", "street","zip_code",\
          "city", "state", "country", "password", "school", "groups"]


class UserSerializer(serializers.ModelSerializer):
   """ Create a serializer to the model user """
   class Meta:
      model=  User
      fields= ["id", "username", "email", "phone_number", "dob", "street",\
               "zip_code","city","state", "country","password", "school", "groups"]

   def create(self, validated_data):
      """ Create a new user and set all fields to the user """
      user= User.objects.create(
         username = validated_data['username'],
         email = validated_data['email'],
         phone_number = validated_data['phone_number'],
         city = validated_data['city'],
         street = validated_data['street'],
         dob = validated_data['dob'],
         zip_code = validated_data['zip_code'],
         country = validated_data['country'],
         state = validated_data['state'],
         school= validated_data['school'],
         groups= validated_data['groups'],
      )
      user.set_password(validated_data['password'])
      user.is_active=False
      user.save()

      """ Send user a  mail to activate his account"""
      current_site = Site.objects.get_current()
      email_subject= "Confirm your Email"
      message2= render_to_string("email_confirmation.html", {
         "name": user.username,
         "domain": current_site.domain,
         "uid": urlsafe_base64_encode(force_bytes(user.pk)),
         "token": generate_token.make_token(user),
      })
      email= EmailMessage(
         email_subject,
         message2,
         settings.EMAIL_HOST_USER,
         [user.email],
      )
      email.fail_silently=True
      email.send()
      return user


class UserUpdateSerializer(serializers.ModelSerializer):
   """ Create a serializer to the model user while update """
   class Meta:
      model=  User
      fields= ["id","username","email", "phone_number", "dob", "street",
      "zip_code", "city", "state", "country","groups","school"]
      read_only_fields= ('username', "email",'password')


class ChangePasswordSeriallizer(serializers.Serializer):
   """Change user password with old password"""
   model=User
   old_password= serializers.CharField(required=True)
   password1= serializers.CharField(required=True)
   password2= serializers.CharField(required=True)


class SendPasswordResetEmailSerializer(serializers.Serializer):
   """Reset your password with email address"""
   email= serializers.EmailField(required=True)
   class Meta:
      model= User
      fields=['email']
         

class ResetNewPasswordSerializer(serializers.Serializer):
   """Set your new password by the link sent on email address"""
   model=User
   password1= serializers.CharField(required=True)
   password2= serializers.CharField(required=True)


class LoginSerializer(serializers.Serializer):
   """login user serializer """
   model = User
   username= serializers.CharField()
   email=    serializers.EmailField()
   password= serializers.CharField()


class LogoutSerializer(serializers.Serializer):
   '''logout users serializer'''
   model=User


