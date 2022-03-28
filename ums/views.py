from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.http import HttpResponse
from django.shortcuts import redirect
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.authtoken.views import ObtainAuthToken
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from userms import settings

from .models import User
from .permissions import CustomPermission
from .serializer import (ChangePasswordSeriallizer,
                         NewPasswordCreateSerializer,
                         PasswordResetEmailSerializer, UserSerializer,
                         UserUpdateSerializer)
from .tokens import generate_token


class UserView(viewsets.ModelViewSet):
   authentication_classes=[TokenAuthentication,SessionAuthentication]
   permission_classes= [CustomPermission]
   filter_backends= [SearchFilter, DjangoFilterBackend]
   filterset_fields=["id","email","username"]
   search_fields=["first_name","last_name"]

   def get_serializer_class(self):
      if self.action=="partial_update" or self.action=="update" or self.action=="retrieve":
         return UserUpdateSerializer
      else:
         return UserSerializer
   def get_queryset(self):
      """Get all data of users in the API when the auper user is logged in """
      if self.request.user.is_superuser:
         return User.objects.all()

      # """Return the data of specific user who is logged in """
      elif self.request.user.is_authenticated:
         return User.objects.filter(pk=self.request.user.id)

      # """ return None if no user is logged in and anonymaous user only can make a post """
      else:
         return User.objects.none()

   def create(self, request, *args, **kwargs):
      """Create a new user """
      data = self.request.data
      serializer= UserSerializer(data=data)
      if serializer.is_valid():
         serializer.save()
         return Response({'message':"Check your email and activate your account!"},status=status.HTTP_201_CREATED)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

def activate(request,uidb64,token):
   """Activate your account by clicking on the link sent to registered amil address"""
   try:
      uid = force_text(urlsafe_base64_decode(uidb64))
      myuser=User.objects.get(pk=uid)
   except (TypeError,ValueError,OverflowError,User.DoesNotExist):
      myuser=None
   if myuser is not None and generate_token.check_token(myuser,token):
      myuser.is_active=True
      myuser.save()
      return redirect("/success")
   else:
      return HttpResponse({"Error":"There is some problem to activate your account."})

class SuccessEmailView(generics.ListAPIView):
   """"""
   """Send the user a success message"""
   def list(self, request, *args, **kwargs):
      data = {
         "details":"Your account has been activated!",
         "login":"You can log in now in login portal!",
      }
      return Response(data,status=status.HTTP_200_OK)

class CustomTokenCreation(ObtainAuthToken):
   def post(self,request,*args, **kwargs):
      response = super(CustomTokenCreation,self).post(request)
      token = Token.objects.get(key= response.data['token'])
      return Response({'key':token.key, "id":token.user_id})


class ChangePasswordView(generics.CreateAPIView):
   serializer_class = ChangePasswordSeriallizer
   permission_classes= [IsAuthenticated,]
   def get_object(self):
      obj = self.request.user
      return obj
   def create(self, request, *args, **kwargs):
      self.object = self.get_object()
      serializer = self.get_serializer(data=request.data)
      if request.data['password1'] == request.data['password2']:
         if serializer.is_valid():
            if not self.object.check_password(serializer.data['old_password']):
               return Response({"Old password":"old password is wrong"},status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data['password1'])
            self.object.save()
            return Response({"message":"your password reset successfully"}, status=status.HTTP_200_OK)
      else:
         return Response({"details":"password1 does not match with password2"},status=status.HTTP_400_BAD_REQUEST)
      return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class RestPasswordEmailView(generics.CreateAPIView):  
   serializer_class = PasswordResetEmailSerializer
   def create(self, request, *args, **kwargs):
      serializer = self.get_serializer(data = request.data)
      if serializer.is_valid():
         try:
            user = User.objects.get(email=serializer.data.get('email'))
         except User.DoesNotExist:
            return Response({"errors":"Provided Email doesn't associate with any User."})
         if user:
            current_site = Site.objects.get_current()
            email_subject= "Password reset Mail"
            message2= render_to_string("pass_reset.html", {
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
         return Response({"detials":"Email has been sent to your registered email address"},status=status.HTTP_200_OK)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class NewPasswordCreateView(generics.CreateAPIView):
   serializer_class = NewPasswordCreateSerializer
   permission_classes=[AllowAny,]
   def create(self, request,uidb64, token):
      serializer = self.get_serializer(data= request.data)
      try:
         token = token
         uid = force_text(urlsafe_base64_decode(uidb64))
         myuser=User.objects.get(pk=uid)
      except User.DoesNotExist:
         myuser= None
      if myuser is not None and generate_token.check_token(myuser,token):
         if serializer.is_valid():
            myuser.set_password(request.data['password1'])
            myuser.save()
            return Response({"details":"Password reset successfully! "},status=status.HTTP_200_OK)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)
