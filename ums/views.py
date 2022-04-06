
from django.contrib.auth import login, logout
from django.contrib.auth.models import Group
from django.contrib.sites.models import Site
from django.core.mail import EmailMessage
from django.db.models import Q
from django.template.loader import render_to_string
from django.utils.encoding import force_bytes, force_text
from django.utils.http import urlsafe_base64_decode, urlsafe_base64_encode
from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import generics, status, viewsets
from rest_framework.authentication import (SessionAuthentication,
                                           TokenAuthentication)
from rest_framework.authtoken.models import Token
from rest_framework.filters import SearchFilter
from rest_framework.permissions import AllowAny, IsAuthenticated,IsAdminUser
from rest_framework.response import Response
from userms import settings

from .models import School, User
from .permissions import CustomPermission,GroupSchoolPermissions
from .serializer import (ChangePasswordSeriallizer, CustomLoginTokenSerializer,
                         Customlogout, GroupSerializer,
                         ResetNewPasswordSerializer, SchoolSerializer,
                         SendPasswordResetEmailSerializer, UserSerializer,
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
         return Response({'Message':"Please check your email to activate your account!"},status=status.HTTP_201_CREATED)
      return Response(serializer.errors,status=status.HTTP_400_BAD_REQUEST)

class SuccessEmailView(generics.ListAPIView):
   """"""
   """Send the user a success message"""
   def list(self,request,uidb64,token):
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

class SendRestPasswordEmailView(generics.CreateAPIView):
   """Forgot your password, enter your mail you will get email to reset password"""
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

class ResetNewPasswordView(generics.CreateAPIView):
   """Check token and reset user password"""
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

class CustomLoginTokenView(generics.CreateAPIView):
   serializer_class= CustomLoginTokenSerializer
   def create(self,request):
      serializer= self.get_serializer(data= request.data)
      if serializer.is_valid():
         try:
            user  = User.objects.get(username=serializer.data.get('username'))
         except:
            return Response({"Oops":"Provided Email or username doesn't associate with any User."})
         if not user.check_password(serializer.data.get('password')):
            return Response({"Errors":"Unable to log in with provided credentials."},status=status.HTTP_400_BAD_REQUEST)
         if not user.is_active:
            return Response({"Errors":"Unable to log in with provided credentials."},status=status.HTTP_400_BAD_REQUEST)
         token,_ = Token.objects.get_or_create(user=user)
         login(request, user)
         return Response({"Token":token.key, "user":token.user_id}, status= status.HTTP_200_OK)
      return Response(serializer.errors)

class CustomLogoutView(generics.CreateAPIView):
   serializer_class= Customlogout
   permission_classes=[IsAuthenticated]
   def create(self,request):
      logout(request)
      return Response({"logout":"logout successfully"})

class SchoolView(viewsets.ModelViewSet):
   """
   Create school
   Only super user can create school and other user can view it only
   """
   serializer_class= SchoolSerializer
   queryset= School.objects.all()
   permission_classes=(GroupSchoolPermissions,)

   def create(self,request,*args, **kwargs):
      serializer= self.get_serializer(data= self.request.data)
      if serializer.is_valid():
         s= School.objects.create(name= serializer.data['name'])
         s.save()
         return Response({"Done":"Created"},status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class GroupView(viewsets.ModelViewSet):
   """Create groups"""
   serializer_class = GroupSerializer
   queryset= Group.objects.all()
   permission_classes=[GroupSchoolPermissions,]

   def create(self,request,*args, **kwargs):
      serializer= self.get_serializer(data= self.request.data)
      if serializer.is_valid():
         s= Group.objects.create(name= serializer.data['name'])
         s.save()
         return Response({"Group":"group Created Successfully"},status=status.HTTP_201_CREATED)
      return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class TeacherListView(generics.ListAPIView):
   serializer_class=UserSerializer
   def get_queryset(self):
      if self.request.user.groups.name=="Coach":
         return User.objects.filter(Q(school= self.request.user.school.id) & ~Q(groups=self.request.user.groups.id))
      if self.request.user.groups.name=="Teachers":
         return User.objects.filter(username= self.request.user.username)
      else:
         return User.objects.none()