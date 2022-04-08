
from django.contrib.auth.models import Group
from rest_framework import serializers

from .models import School, User


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
      fields= [ "id", "username", "email", "phone_number", "dob", "street","zip_code",
               "city", "state", "country", "school", "groups"]


class UserCreateSerializer(serializers.ModelSerializer):
   """ Create a serializer to the model user """
   class Meta:
      model=  User
      fields= ["id", "username", "email", "phone_number", "dob", "street",
               "zip_code","city","state", "country","password", "school", "groups"]


class UserUpdateSerializer(serializers.ModelSerializer):
   """ Create a serializer to the model user while update """
   class Meta:
      model=  User
      fields= [ "id","username","email", "phone_number", "dob", "street",
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
   '''logout user serializer'''
   model=User
