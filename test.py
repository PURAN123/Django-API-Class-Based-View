

# from django.contrib.auth.models import Group
# from django.urls import reverse
# from rest_framework import status
# from rest_framework.authtoken.models import Token
# from rest_framework.test import APITestCase

# from ums.models import School, User


# class CustomUnAuthorizeTestCase(APITestCase):
# #    """ All test cases for the un-authenticated user """
#    def setUp(self):
# #       """ Create users to test your code """
#       self.group = Group.objects.create(
#          name= "name"
#       )
#       self.school = School.objects.create(
#          name= "name"
#       )
# #       self.user1 = User.objects.create_user( username= "test",
# #          email= "test.test.1002.2001@gmail.com",
# #          phone_number= "01231231230",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #          school= self.school,
# #          groups= self.group
# #       )
# #       self.user2 = User.objects.create_user( username= "test1",
# #          email= "test.test.1002.20@gmail.com",
# #          phone_number= "01231231000",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #          school= self.school,
# #          groups= self.group
# #       )

#    # def test_post_unauthnticated_user(self):
#    #    """The user can only post the data for registration """ 
#    #    data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
#    #    "dob": "2001-03-03", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
#    #    "country": "India", "password": "password","school":self.school,"groups": self.group
#    #    }
#    #    response = self.client.post(reverse("users-list"), data=data)
#    #    self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# #    def test_unauthnticated_view_user(self):
# #       """The user has not permissions to view details of user"""
# #       response = self.client.get(reverse("users-detail",kwargs={"pk":self.user1.id}))
# #       self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# #    def test_unauthnticated_update_details(self):
# #       """The user has not permissions to update details of user"""
# #       data = {"zip_code": 246268, "city": "Washington", "state": "California", "country": "Amerika"}
# #       response= self.client.put(reverse("users-detail", kwargs={'pk':self.user1.id}),data=data)
# #       self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# #    def test_unauthnticated_delete_user(self):
# #       """The user has not permissions to delete the user"""
# #       url = reverse("users-detail",kwargs={"pk": self.user1.pk})
# #       response =  self.client.delete(url)
# #       self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)



# # class AuthenticatedUserTestCase(APITestCase):
# #    def setUp(self):
# #       self.group = Group.objects.create(
# #          name= "name"
# #       )
# #       self.school = School.objects.create(
# #          name= "name"
# #       )
# #       self.user1 = User.objects.create_user( username= "test",
# #          email= "test.test.1002.2001@gmail.com",
# #          phone_number= "01231231230",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #          school= self.school,
# #          groups= self.group
# #       )
# #       self.user2 = User.objects.create_user( username= "test1",
# #          email= "test.test.1002.20@gmail.com",
# #          phone_number= "01231231000",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #          school= self.school,
# #          groups= self.group
# #       )   
# #    def test_authenticated_post_user(self):
# #       """The authenticated user has not permissions to post details for registration"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
# #       "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
# #       "country": "India", "password": "password"
# #       }
# #       response = self.client.post(reverse("users-list"), data=data, format="json")
# #       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# #    def test_authenticated_get_own_details(self):
# #       """Authenticated user can get its own data only"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.get(reverse("users-detail",kwargs={"pk":self.user1.id}))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)
# #    def test_authenticated_get_other_user_details(self):
# #       """Authenticated user can not get other user data"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.get(reverse("users-detail",kwargs={"pk":self.user2.id}))
# #       self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

# #    def test_authenticated_update_own_data(self):
# #       """ The user has permissions to update details of own"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
# #       "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
# #       "country": "India", "password": "password"
# #       }
# #       response= self.client.put(reverse("users-detail", kwargs={'pk':self.user1.id}),data=data)
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)
# #    def test_authenticated_update_other_user_data(self):
# #       """ The user has not permissions to update details of other user"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
# #       "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
# #       "country": "India", "password": "password"
# #       }
# #       response= self.client.put(reverse("users-detail", kwargs={'pk':self.user2.id}),data=data)
# #       self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
   
# #    def test_authenticated_delete_own_user(self):
# #       """Authenticated user can delete its own data only not other user data"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       url = reverse("users-detail",kwargs={"pk": self.user1.pk})
# #       response =  self.client.delete(url)
# #       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
# #    def test_authenticated_delete_other_user(self):
# #       """
# #       Authenticated user can delete its own data only not other user data
# #       """
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       url = reverse("users-detail",kwargs={"pk": self.user2.pk})
# #       response =  self.client.delete(url)
# #       self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


# # class SuperUserTestCase(APITestCase):
# #    """
# #    Test conditions for super user
# #    """
# #    def setUp(self):
# #       self.superuser = User.objects.create_superuser( username= "test",
# #          email= "test.test.1002.2001@gmail.com",
# #          phone_number= "01231231230",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password"
# #       )
# #       self.user2 = User.objects.create_user( username= "test1",
# #          email= "test.test.1002.20@gmail.com",
# #          phone_number= "01231231000",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password"
# #       )   
# #    def test_superuser_for_post_user(self):
# #       """Super user can not post any data for registrations"""
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
# #       "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
# #       "country": "India", "password": "password"
# #       }
# #       response = self.client.post(reverse("users-list"), data=data, format="json")
# #       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# #    def test_superuser_for_get_user_data(self):
# #       """Super user can access every user data"""
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.get(reverse("users-detail",kwargs={"pk":self.user2.id}))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)
# #    def test_superuser_for_get_superuser_data(self):
# #       """Super user can access own data"""
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.get(reverse("users-detail",kwargs={"pk":self.superuser.id}))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_superuser_for_update_user_data(self):
# #       """Super user can update every user data"""
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
# #       "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
# #       "country": "India", "password": "password"
# #       }
# #       response= self.client.put(reverse("users-detail", kwargs={'pk':self.user2.id}),data=data)
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)
# #    def test_superuser_for_update_own_data(self):
# #       """Super user can update own data"""
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
# #          "dob":"2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore",
# #          "state": "Karnataka", "country": "India", "password": "password"
# #       }
# #       response= self.client.put(reverse("users-detail", kwargs={'pk':self.superuser.id}),data=data)
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_superuser_for_delete_user_data(self):
# #       """Super user can delete every user data"""
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       url = reverse("users-detail",kwargs={"pk": self.user2.pk})
# #       response =  self.client.delete(url)
# #       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
# #    def test_superuser_for_delete_superuser_data(self):
# #       """Super user can delete own data"""
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       url = reverse("users-detail",kwargs={"pk": self.superuser.pk})
# #       response =  self.client.delete(url)
# #       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)


# # class PasswordResetUpdate(APITestCase):
# #    """Password related tasks"""
# #    def setUp(self):
# #       self.user1 = User.objects.create_user( username= "test",
# #          email= "test.test.1002.2001@gmail.com",
# #          phone_number= "01231231230",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password"
# #       )

# #    def test_for_forgot_password_send_mail(self):
# #       """Forgot your password, enter your mail you will get email to reset password"""
# #       data = {
# #          'email' : "user@gmail.com",
# #       }
# #       response= self.client.post(reverse("reset-password"), data= data)
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)
   
# #    def test_for_change_password(self):
# #       """Change your password but you should have your old password"""
# #       data = {
# #          "old_password":"password",
# #          "password1":"change",
# #          "password2":"change"
# #       }
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response= self.client.post(reverse("change-password"), data= data)
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)


# # class LoginLogoutTestCase(APITestCase):
# #    def setUp(self):
# #       self.user1 = User.objects.create_user(
# #          username= "test",
# #          email= "test.test.1002.2001@gmail.com",
# #          phone_number= "01231231230",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password"
# #       )

# #    def test_user_login_view(self):
# #       """User login """
# #       data= {
# #          'username':'test',
# #          'email':"test.test@gmail.com",
# #          'password':'password'
# #       }
# #       response = self.client.post(reverse('login'),data=data)
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_user_logout_view(self):
# #       """User logout"""
# #       token= Token.objects.create(user=self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.post(reverse('logout'),data={})
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)



# # class GroupTestCasesForAllUsers(APITestCase):
# #    def setUp(self):
# #       self.superuser = User.objects.create_superuser( username= "test",
# #          email= "test.test.1002.2001@gmail.com",
# #          phone_number= "01231231230",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #       )
# #       self.user1 = User.objects.create_user( username= "test1",
# #          email= "test.test.1002.20@gmail.com",
# #          phone_number= "01231231000",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #       )
# #       self.group = Group.objects.create(
# #          name= "name"
# #       )
# #    def test_group_post_for_superuser(self):
# #       """Super user can post the new group only """
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.post(reverse("group-list"),data= {"name":"nam"})
# #       self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# #    def test_group_get_for_superuser(self):
# #       """super user can see all groups"""
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.get(reverse("group-list"))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_group_update_for_superuser(self):
# #       """Super user can update the groups only """
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.put(reverse("group-detail",kwargs={"pk":self.group.id}),data= {'name':'name'})
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_group_delete_for_superuser(self):
# #       """Super user can delete the group only """
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.delete(reverse("group-detail",kwargs={"pk":self.group.id}))
# #       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# # # For Authenticated user 
# #    def test_group_post_case_for_authenticate(self):
# #       """Authenticated user can not post the new groups"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.post(reverse("group-list"),data= {'name':'name'})
# #       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# #    def test_group_get_case_for_authenticate(self):
# #       """authenticated user can see the groups """
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.get(reverse("group-list"))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_group_update_for_authenticate(self):
# #       """authenticate user can not update the group"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.put(reverse("group-detail",kwargs={"pk":self.group.id}),data= {'name':'nam'})
# #       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# #    def test_group_delete_for_authenticate(self):
# #       """authenticate user can delete the group """
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.delete(reverse("group-detail",kwargs={"pk":self.group.id}))
# #       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# # # For anonymous user
# #    def test_group_post_for_anonymous(self):
# #       """Anonymous user can not post the new group """
# #       response = self.client.post(reverse("group-list"),data= {'name':'name'})
# #       self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# #    def test_group_get_for_anonymous(self):
# #       """anonymous user can not see the groups """
# #       response = self.client.get(reverse("group-list"))
# #       self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# #    def test_group_update_for_anonymous(self):
# #       """Anonymous user can not update group """
# #       response = self.client.put(reverse("group-detail",kwargs={"pk":self.group.id}),data= {'name':'nam'})
# #       self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# #    def test_group_delete_for_anonymous(self):
# #       """Anonymous user can not delete group """
# #       response = self.client.delete(reverse("group-detail",kwargs={"pk":self.group.id}))
# #       self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



# # class SchoolTestCasesForAllUsers(APITestCase):
# #    def setUp(self):
# #       self.superuser = User.objects.create_superuser( username= "test",
# #          email= "test.test.1002.2001@gmail.com",
# #          phone_number= "01231231230",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #       )
# #       self.user1 = User.objects.create_user( username= "test1",
# #          email= "test.test.1002.20@gmail.com",
# #          phone_number= "01231231000",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #       )
# #       self.school = School.objects.create( 
# #          name= "Primary" 
# #       )

# #    def test_school_post_for_superuser(self):
# #       """Super user can post the new school only """
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.post(reverse("school-list"),data= {"name":"nam"})
# #       self.assertEqual(response.status_code, status.HTTP_201_CREATED)

# #    def test_school_get_for_superuser(self):
# #       """super user can see all schools"""
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.get(reverse("school-list"))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_school_update_for_superuser(self):
# #       """Super user can update the schools only """
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.put(reverse("school-detail",kwargs={"pk":self.school.id}),data= {'name':'name'})
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_school_delete_for_superuser(self):
# #       """Super user can delete the school only """
# #       token = Token.objects.create(user = self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.delete(reverse("school-detail",kwargs={"pk":self.school.id}))
# #       self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

# # # For Authenticated user 
# #    def test_school_post_for_authenticate(self):
# #       """Authenticated user can not post the new school"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.post(reverse("school-list"),data= {'name':'name'})
# #       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# #    def test_school_get_for_authenticate(self):
# #       """authenticated user can see the school """
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.get(reverse("school-list"))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_school_update_for_authenticate(self):
# #       """authenticate user can not update the school"""
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.put(reverse("school-detail",kwargs={"pk":self.school.id}),data= {'name':'nam'})
# #       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# #    def test_school_delete_for_authenticate(self):
# #       """authenticate user can delete the school """
# #       token = Token.objects.create(user = self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response = self.client.delete(reverse("school-detail",kwargs={"pk":self.school.id}))
# #       self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

# # # For anonymous user
# #    def test_school_post_for_anonymous(self):
# #       """Anonymous user can not post the new school """
# #       response = self.client.post(reverse("school-list"),data= {'name':'name'})
# #       self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# #    def test_school_get_for_anonymous(self):
# #       """anonymous user can not see the school """
# #       response = self.client.get(reverse("group-list"))
# #       self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# #    def test_school_update_for_anonymous(self):
# #       """Anonymous user can not update school """
# #       response = self.client.put(reverse("school-detail",kwargs={"pk":self.school.id}),data= {'name':'nam'})
# #       self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

# #    def test_school_delete_for_anonymous(self):
# #       """Anonymous user can not delete school """
# #       response = self.client.delete(reverse("school-detail",kwargs={"pk":self.school.id}))
# #       self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)



# # class TeacherAndCoachTestCase(APITestCase):
# #    """All test cases for to get teacher When coach is login and return teacher instance if
# #    teacher is login and for super user all user will be returned
# #    """
# #    def setUp(self):
# #       self.group = Group.objects.create(
# #          name= "name"
# #       )
# #       self.school = School.objects.create(
# #          name= "name"
# #       )
# #       self.superuser = User.objects.create_superuser( username= "test",
# #          email= "test.test.1002.2001@gmail.com",
# #          phone_number= "01231231230",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #          school= self.school,
# #          groups= self.group
# #       )
# #       self.user1 = User.objects.create_user( username= "test1",
# #          email= "test.test.1002.20@gmail.com",
# #          phone_number= "01231231000",
# #          dob= "2022-03-02",
# #          street= "231",
# #          zip_code= 246285,
# #          city= "Banglore",
# #          state= "Karnataka",
# #          country= "India",
# #          password= "password",
# #          school= self.school,
# #          groups= self.group
# #       )
# #    def test_get_teacher_by_super_user(self):
# #       token= Token.objects.create(user=self.superuser)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response= self.client.get(reverse('users-list'))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_get_teacher_by_coach_User(self):
# #       token= Token.objects.create(user=self.user1)
# #       self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
# #       response= self.client.get(reverse('users-list'))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)

# #    def test_get_teacher_by_teacher_user(self):
# #       response= self.client.get(reverse('users-list'))
# #       self.assertEqual(response.status_code, status.HTTP_200_OK)



# # Is school CRUD test cases have a different  class or Add it on in a same class where I have created User CRUD test cases.