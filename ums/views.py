
from django.contrib.auth import login, logout
from django.contrib.auth.hashers import make_password
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage, send_mail
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.response import Response
from userms import settings

from .models import School, User
from .permissions import SchoolAndGroupPermissions, UserPermissions
from .serializer import (ChangePasswordSeriallizer, GroupSerializer,
                         LoginSerializer, LogoutSerializer,
                         ResetNewPasswordSerializer, SchoolSerializer,
                         SendPasswordResetEmailSerializer, UserListSerializer,
                         UserSerializer, UserUpdateSerializer)
from .tokens import generate_token


class UserView(viewsets.ModelViewSet):
   """User view which will return the user as logged in user's permissions"""
   authentication_classes=[TokenAuthentication,SessionAuthentication]
   permission_classes= [UserPermissions]
   filter_backends= [SearchFilter, DjangoFilterBackend]
   filterset_fields=["id","email","username"]
   search_fields=["first_name","last_name"]

   def get_serializer_class(self):
      """Return specific serializer according to requirement"""
      if self.action== 'create':
         return UserSerializer
      if self.action== 'update':
         return UserUpdateSerializer
      return UserListSerializer

   def get_queryset(self):
      """ Get users sccording to permissions of user """
      if self.request.user.is_superuser:
         return User.objects.all()
      elif self.request.user.is_authenticated and self.request.user.groups == None:
         """Authenticate user can see his data"""
         return User.objects.filter(pk=self.request.user.id)
      elif self.request.user.groups.name=="Coach":
         """Coach can see all teachers and coach of same school"""
         return User.objects.filter(school= self.request.user.school.id)
      elif self.request.user.groups.name=="Teacher":
         """Teacher can see only  his data"""
         return User.objects.filter(username= self.request.user.username)
      else:
         return User.objects.none()

   def create(self, request, *args, **kwargs):
      """Create a new user """
      serializer= UserSerializer(data=self.request.data)
      if serializer.is_valid():
         serializer.save(is_active=False,password= make_password(serializer.validated_data['password']))
         activate_account(serializer.data['email'])
         return Response({'Message':"Please check your email to activate your account!"},\
                           status=status.HTTP_201_CREATED)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class AccountActivatedView(generics.ListAPIView):
   """Send the user a success message"""
   def list(self,request,uidb64,token):
      """Show usera success message """
      try:
         uid = force_text(urlsafe_base64_decode(uidb64))
         myuser=User.objects.get(pk=uid)
      except (TypeError,ValueError,OverflowError,User.DoesNotExist):
         myuser=None
      if myuser is not None and generate_token.check_token(myuser,token):
         myuser.is_active=True
         myuser.save()
         return Response({"Success":"Your account has been activated successfully","Note":"You can login in login portal"},status=status.HTTP_200_OK)
      else:
         return Response({'Oops':"There is some problem to activate your account"})


class ChangePasswordView(generics.CreateAPIView):
   """Change your password but you should have your old password"""
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
               return Response({"Oops":"Old password is wrong"},status=status.HTTP_400_BAD_REQUEST)
            self.object.set_password(serializer.data['password1'])
            self.object.save()
            return Response({"success":"Your password reset successfully"}, status=status.HTTP_200_OK)
      else:
         return Response({"Oops":"Password1 does not match with Password2"},status=status.HTTP_400_BAD_REQUEST)
      return Response(serializer.errors,status=status.HTTP_404_NOT_FOUND)


class SendResetPasswordEmailView(generics.CreateAPIView):
   """If you Forgot your password reset password by your email address """
   serializer_class = SendPasswordResetEmailSerializer
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


class ResetPasswordView(generics.CreateAPIView):
   """Check user and token and reset user password"""
   serializer_class = ResetNewPasswordSerializer
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
            if not serializer.data['password1']==serializer.data['password2']:
               return Response({"Errors":"Oops, password1 and password2 are not same"})
            myuser.set_password(request.data['password1'])
            myuser.save()
            return Response({"success":"Password reset successfully! "},status=status.HTTP_200_OK)
         return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)


class LoginView(generics.CreateAPIView):
   """Login a user by its username,email and password and return its token and id"""
   serializer_class= LoginSerializer
   def create(self,request):
      serializer= self.get_serializer(data= request.data)
      if serializer.is_valid():
         try:
            user  = User.objects.get(username=serializer.data.get('username'))
         except:
            return Response({"error":"Provided Email or username doesn't associate with any User."})
         if not user.check_password(serializer.data.get('password')):
            return Response({"Errors":"Unable to log in with provided credentials."},status=status.HTTP_400_BAD_REQUEST)
         if not user.is_active:
            return Response({"Errors":"Unable to log in with provided credentials."},status=status.HTTP_400_BAD_REQUEST)
         token,_ = Token.objects.get_or_create(user=user)
         login(request, user)
         return Response({"user":token.user_id,"Token":token.key}, status= status.HTTP_200_OK)
      return Response(serializer.errors)


class LogoutView(generics.CreateAPIView):
   """ Logout user which is already logged in """
   serializer_class= LogoutSerializer
   permission_classes=[IsAuthenticated]
   def create(self,request):
      logout(request)
      return Response({"logout":"logout successfully"})


class SchoolView(viewsets.ModelViewSet):
   """School model view"""
   serializer_class= SchoolSerializer
   queryset= School.objects.all()
   permission_classes=[SchoolAndGroupPermissions,]


class GroupView(viewsets.ModelViewSet):
   """Group model View """
   serializer_class = GroupSerializer
   queryset= Group.objects.all()
   permission_classes=[SchoolAndGroupPermissions,]


def activate_account(email):
   """ Send user an email to activate his account """
   try:
      user= User.objects.get(email= email)
   except:
      return 
   current_site = Site.objects.get_current()
   email_subject= "Confirm your Email"
   message= render_to_string("email_confirmation.html", {
      "name": user.username,
      "domain": current_site.domain,
      "uid": urlsafe_base64_encode(force_bytes(user.id)),
      "token": generate_token.make_token(user),
   })
   email= EmailMessage(
      email_subject,
      message,
      settings.EMAIL_HOST_USER,
      [user.email],
   )
   email.fail_silently=True
   email.send()

