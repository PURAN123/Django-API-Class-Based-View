
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from .models import User

class CustomUnAuthorizeTestCase(APITestCase):
   """
   All test cases for the un-authenticated user
   """
   def setUp(self):
      """
      Create users to test your code
      """
      self.user1 = User.objects.create_user( username= "test",
         email= "test.test.1002.2001@gmail.com",
         phone_number= "01231231230",
         dob= "2022-03-02",
         street= "231",
         zip_code= 246285,
         city= "Banglore",
         state= "Karnataka",
         country= "India",
         password= "password"
      )
      self.user2 = User.objects.create_user( username= "test1",
         email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000",
         dob= "2022-03-02",
         street= "231",
         zip_code= 246285,
         city= "Banglore",
         state= "Karnataka",
         country= "India",
         password= "password"
      )

   def test_post_unauthnticated_user(self):
      """The user can only post the data for registration """ 
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
      "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
      "country": "India", "password": "password"
      }
      response = self.client.post(reverse("users-list"), data=data, format="json")
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_unauthnticated_view_user(self):
      """The user has not permissions to view details of user"""
      response = self.client.get(reverse("users-detail",kwargs={"pk":self.user1.id}))
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   def test_unauthnticated_update_details(self):
      """The user has not permissions to update details of user"""
      data = {"zip_code": 246268, "city": "Washington", "state": "California", "country": "Amerika"}
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.user1.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   def test_unauthnticated_delete_user(self):
      """The user has not permissions to delete the user"""
      url = reverse("users-detail",kwargs={"pk": self.user1.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



class AuthenticatedUserTestCase(APITestCase):
   def setUp(self):
      self.user1 = User.objects.create_user( username= "test",
         email= "test.test.1002.2001@gmail.com",
         phone_number= "01231231230",
         dob= "2022-03-02",
         street= "231",
         zip_code= 246285,
         city= "Banglore",
         state= "Karnataka",
         country= "India",
         password= "password"
      )
      self.user2 = User.objects.create_user( username= "test1",
         email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000",
         dob= "2022-03-02",
         street= "231",
         zip_code= 246285,
         city= "Banglore",
         state= "Karnataka",
         country= "India",
         password= "password"
      )   
   def test_authenticated_post_user(self):
      """The authenticated user has not permissions to post details for registration"""
      token = Token.objects.create(user = self.user1)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
      "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
      "country": "India", "password": "password"
      }
      response = self.client.post(reverse("users-list"), data=data, format="json")
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_authenticated_get_own_details(self):
      """Authenticated user can get its own data only"""
      token = Token.objects.create(user = self.user1)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("users-detail",kwargs={"pk":self.user1.id}))
      self.assertEqual(response.status_code, status.HTTP_200_OK)
   def test_authenticated_get_other_user_details(self):
      """Authenticated user can not get other user data"""
      token = Token.objects.create(user = self.user1)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("users-detail",kwargs={"pk":self.user2.id}))
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   def test_authenticated_update_own_data(self):
      """ The user has permissions to update details of own"""
      token = Token.objects.create(user = self.user1)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
      "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
      "country": "India", "password": "password"
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.user1.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
   def test_authenticated_update_other_user_data(self):
      """ The user has not permissions to update details of other user"""
      token = Token.objects.create(user = self.user1)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
      "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
      "country": "India", "password": "password"
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.user2.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
   
   def test_authenticated_delete_own_user(self):
      """Authenticated user can delete its own data only not other user data"""
      token = Token.objects.create(user = self.user1)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.user1.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
   def test_authenticated_delete_other_user(self):
      """
      Authenticated user can delete its own data only not other user data
      """
      token = Token.objects.create(user = self.user1)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.user2.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class SuperUserTestCase(APITestCase):
   """
   Test conditions for super user
   """
   def setUp(self):
      self.superuser = User.objects.create_superuser( username= "test",
         email= "test.test.1002.2001@gmail.com",
         phone_number= "01231231230",
         dob= "2022-03-02",
         street= "231",
         zip_code= 246285,
         city= "Banglore",
         state= "Karnataka",
         country= "India",
         password= "password"
      )
      self.user2 = User.objects.create_user( username= "test1",
         email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000",
         dob= "2022-03-02",
         street= "231",
         zip_code= 246285,
         city= "Banglore",
         state= "Karnataka",
         country= "India",
         password= "password"
      )   
   def test_superuser_for_post_user(self):
      """Super user can not post any data for registrations"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
      "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
      "country": "India", "password": "password"
      }
      response = self.client.post(reverse("users-list"), data=data, format="json")
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_superuser_for_get_user_data(self):
      """Super user can access every user data"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("users-detail",kwargs={"pk":self.user2.id}))
      self.assertEqual(response.status_code, status.HTTP_200_OK)
   def test_superuser_for_get_superuser_data(self):
      """Super user can access own data"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("users-detail",kwargs={"pk":self.superuser.id}))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_superuser_for_update_user_data(self):
      """Super user can update every user data"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
      "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
      "country": "India", "password": "password"
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.user2.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
   def test_superuser_for_update_own_data(self):
      """Super user can update own data"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
         "dob":"2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore",
         "state": "Karnataka", "country": "India", "password": "password"
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.superuser.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_superuser_for_delete_user_data(self):
      """Super user can delete every user data"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.user2.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
   def test_superuser_for_delete_superuser_data(self):
      """Super user can delete own data"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.superuser.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


class LoginApiCustomize(APITestCase):
   """log in user"""
   def setUp(self):
      self.user1 = User.objects.create_user( username= "test",
         email= "user1@gmail.com",
         phone_number= "01231231230",
         dob= "2022-03-02",
         street= "231",
         zip_code= 246285,
         city= "Banglore",
         state= "Karnataka",
         country= "India",
         password= "password"
      )

   def test_login_user_page(self):
      data = {
         "username" : "test",
         'email' : "test.test.1002.2001@gmail.com",
         'password' : "password"
      }
      response= self.client.post(reverse("rest_login"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
   
   def test_logout_user_page(self):
      response= self.client.post(reverse("rest_logout"), data= {})
      self.assertEqual(response.status_code, status.HTTP_200_OK)


class PasswordResetUpdate(APITestCase):
   """Password related tasks"""
   def setUp(self):
      self.user1 = User.objects.create_user( username= "test",
         email= "test.test.1002.2001@gmail.com",
         phone_number= "01231231230",
         dob= "2022-03-02",
         street= "231",
         zip_code= 246285,
         city= "Banglore",
         state= "Karnataka",
         country= "India",
         password= "password"
      )

   def test_for_forgot_password_send_mail(self):
      """Forgot your password, enter your mail you will get email to reset password"""
      data = {
         'email' : "user@gmail.com",
      }
      response= self.client.post(reverse("password-reset"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
   
   def test_for_change_password(self):
      """Change your password but you should have your old password"""
      data = {
         "old_password":"password",
         "password1":"change",
         "password2":"change"
      }
      token = Token.objects.create(user = self.user1)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.post(reverse("change-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

class LoginLogoutTestCase(APITestCase):
   def setUp(self):
      self.user1 = User.objects.create_user(
         username= "test",
         email= "test.test.1002.2001@gmail.com",
         phone_number= "01231231230",
         dob= "2022-03-02",
         street= "231",
         zip_code= 246285,
         city= "Banglore",
         state= "Karnataka",
         country= "India",
         password= "password"
      )

   def test_user_login_view(self):
      data= {
         'username':'test',
         'email':"test.test@gmail.com",
         'password':'password'
      }
      response = self.client.post(reverse('login'),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
   def test_user_logout_view(self):
      token= Token.objects.create(user=self.user1)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse('logout'),data={})
      self.assertEqual(response.status_code, status.HTTP_200_OK)
