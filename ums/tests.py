
from django.contrib.auth.models import Group
from django.urls import reverse
from rest_framework import status
from rest_framework.authtoken.models import Token
from rest_framework.test import APITestCase

from ums.models import School, User


class CreateUserTestCases(APITestCase):
   """ Register users test cases for all types of user """
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city= "Banglore",state= "Karnataka",country= "India",
         password= "password",school= self.school, groups= self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",email= "test1@gmail.com",
         phone_number=   "01231231",dob= "2022-03-02",street= "231",
         zip_code= 246285,city= "Banglore",state= "Karnataka",country= "India",
         password= "password",school= self.school, groups= self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test2@gmail.com",
         phone_number=   "0123131",dob= "2022-03-02",street= "231",
         zip_code= 246285,city= "Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231", 
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school= self.school, groups= self.coach_group
      )

   def test_register_anonymous_user(self):
      """The anonymous user can post the data for registration """ 
      data = {"username": "test3", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
               "dob": "2001-03-03", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
               "country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      response = self.client.post(reverse("users-list"), data=data)
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_register_user_by_authnticated_user(self):
      """The authenticated user has no permissions to post details for registration"""
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
               "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore",
               "state": "Karnataka", "country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      response = self.client.post(reverse("users-list"), data=data, format="json")
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   
   def test_register_user_by_super_user(self):
      """Super user can not post any data for registrations"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
               "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore",
               "state": "Karnataka","country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      response = self.client.post(reverse("users-list"), data=data, format="json")
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_register_user_by_coach_user(self):
      """The coach user can not post an user"""
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
               "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore",
               "state": "Karnataka", "country": "India", "password": "password",'school':self.school.id,"groups":self.coach_group.id
      }
      response = self.client.post(reverse("users-list"), data=data, format="json")
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_register_user_by_teacher_user(self):
      """The teacher user can not post an user"""
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {"username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
               "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore",
               "state": "Karnataka", "country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      response = self.client.post(reverse("users-list"), data=data, format="json")
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   

class UpdateUserTestCases(APITestCase):
   def setUp(self):
      """ Update users to test your code """
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      self.teacher_user = User.objects.create_user(
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city= "Banglore",state= "Karnataka",
         country= "India",password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test2@gmail.com",
         phone_number=   "0123131",dob= "2022-03-02",street= "231",
         zip_code= 246285,city= "Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )

   def test_update_user_details_by_anonymous_user(self):
      """The anonymous user has no permissions to update details of user"""
      data = {
         "username": "test","email": "test.test.1002.2001@gmail.com",
         "phone_number":   "01231231230","dob": "2022-03-02","street": "231",
         "zip_code": 246285,"city": "Banglore","state":"Karnataka",
         "country":"India","password": "password","school":self.school,"groups":self.coach_group.id
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.teacher_user.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   def test_update_user_details_of_self_by_authenticate(self):
      """ The user has permissions to update his own details"""
      data = {
         "username": "test", "email": "test.test.1002.2001@gmail.com", "phone_number":"20202020",
         "dob": "2001-5-3", "street": "56", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
         "country": "India", "password": "password","school":self.school.id,"groups":self.teacher_group.id
      }
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.authenticate_user.id}),data=data,format='json')
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_update_user_details_by_other_user(self):
      """ The user has not permissions to update details of other user"""
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {
         "username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
         "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
         "country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.coach_user.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   def test_update_user_details_by_superuser(self):
      """Super user can update every user data"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {
         "username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
         "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
         "country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.coach_user.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_update_superuser_details_by_superuser(self):
      """Super user can update own data"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {
         "username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
         "dob":"2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore",
         "state": "Karnataka", "country": "India", "password": "password",'school':self.school.id,"groups":self.coach_group.id
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.superuser.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_update_user_details_by_coachuser_self(self):
      """ The coach user has permissions to update details of own"""
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {
         "username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
         "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
         "country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.coach_user.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_update_user_details_by_coachuser_of_other_user(self):
      """ The coach user has not permissions to update details of other user"""
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {
         "username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
         "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
         "country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.teacher_user.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


   def test_update_user_details_by_teacheruser_of_self(self):
      """ The Teacher user has permissions to update details of own"""
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      data = {
         "username": "test2", "email": "test.test.2001.1002@gmail.com", "phone_number":"20202020",
         "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
         "country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.teacher_user.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_update_user_details_by_teacher_of_other_user(self):
      """ The teacher user has not permissions to update details of other user"""
      data = {
         "username": "test2", "email": "test.test.1002.20@gmail.com", "phone_number":"01231231000",
         "dob": "2001-3-3", "street": "232", "zip_code": 246268,"city": "Banglore", "state": "Karnataka",
         "country": "India", "password": "password",'school':self.school.id,"groups":self.teacher_group.id
      }
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.put(reverse("users-detail", kwargs={'pk':self.authenticate_user.id}),data=data)
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class DeleteUserTestCases(APITestCase):
   def setUp(self):
      """ Update users to test your code """
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      self.teacher_user = User.objects.create_user(
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number= "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city= "Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school, groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.2001@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test2@gmail.com",
         phone_number=   "0123131",dob= "2022-03-02",street= "231",
         zip_code= 246285,city= "Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )

   def test_delete_user_by_anonymous(self):
      """The user has not permissions to delete the user"""
      url = reverse("users-detail",kwargs={"pk": self.teacher_user.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   def test_delete_authenticate_user_own_details(self):
      """Authenticated user can delete its own data only"""
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.authenticate_user.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

   def test_delete_user_details_by_other_user(self):
      """ Authenticated user can not delete other user data """
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.coach_user.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

   def test_delete_user_by_superuser(self):
      """ Super user can delete every user data """
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.coach_user.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

   def test_delete_superuseruser_details_by_superuser(self):
      """ Super user can delete own data """
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.superuser.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

   def test_delete_user_details_by_coach_user_of_other_user(self):
      """ Coach user can not delete other user data """
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.teacher_user.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_delete_user_details_by_coach_self(self):
      """ Coach user can delete his own data """
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.coach_user.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
     

   def test_delete_user_details_by_teacher_self(self):
      """ Coach user can delete his own data """
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.teacher_user.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

   def test_delete_user_details_by_teacher_otheruser(self):
      """ Coach user can delete his own data """
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      url = reverse("users-detail",kwargs={"pk": self.coach_user.pk})
      response =  self.client.delete(url)
      self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)


class ListUserTestCases(APITestCase):
   def setUp(self):
      """ Update users to test your code """
      self.school= School.objects.create(name='name')
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city= "Banglore",state= "Karnataka",
         country= "India",password= "password",school=self.school, groups=self.teacher_group
      )

      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )

      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_list_all_users_for_anonymous_user(self):
         """The user has not permissions to view details of users"""
         response= self.client.get(reverse("users-list"))
         self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_list_all_users_for_autheticate_user(self):
         """The user has not permissions to view details of own"""
         token = Token.objects.create(user = self.teacher_user)
         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
         response= self.client.get(reverse("users-list"))
         self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_list_all_users_for_superuser_user(self):
         """ The user has not permissions to view details of own """
         token = Token.objects.create(user = self.superuser)
         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
         response= self.client.get(reverse("users-list"))
         self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_list_all_users_for_coach_user(self):
         """ coach user can view all teachers in in school """
         token = Token.objects.create(user = self.coach_user)
         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
         response= self.client.get(reverse("users-list"))
         self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_list_teacher_user_for_teacher_user(self):
         """ The user has not permissions to view details of own """
         token = Token.objects.create(user = self.teacher_user)
         self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
         response= self.client.get(reverse("users-list"))
         self.assertEqual(response.status_code, status.HTTP_200_OK)


class CreateGroupTestCases(APITestCase):
   """Create group test cases"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_group_create_by_superuser(self):
      """Super user can post the new group """
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse("group-list"),data= {"name":"nam"})
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_group_create_by_authenticate_user(self):
      """Authenticated user can not post the new groups"""
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse("group-list"),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_post_by_anonymous_user(self):
      """Anonymous user can not post the new group """
      response = self.client.post(reverse("group-list"),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_group_create_by_coach_user(self):
      """coach user can not post the new groups"""
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse("group-list"),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_create_by_teacher_user(self):
      """teacher user can not create the groups"""
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse("group-list"),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UpdateGroupTestCases(APITestCase):
   """Update group test cases"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )
   def test_group_update_for_superuser(self):
      """Super user can update the groups only """
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.put(reverse("group-detail",kwargs={"pk":self.teacher_group.id}),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_group_update_for_authenticate_user(self):
      """authenticate user can not update the group"""
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.put(reverse("group-detail",kwargs={"pk":self.teacher_group.id}),data= {'name':'nam'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_update_for_anonymous_user(self):
      """Anonymous user can not update group """
      response = self.client.put(reverse("group-detail",kwargs={"pk":self.teacher_group.id}),data= {'name':'nam'})
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_group_update_for_teacher_user(self):
      """Teacher user can not update the group"""
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.put(reverse("group-detail",kwargs={"pk":self.teacher_group.id}),data= {'name':'nam'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_update_for_coach_user(self):
      """Coach user can not update the group"""
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.put(reverse("group-detail",kwargs={"pk":self.teacher_group.id}),data= {'name':'nam'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
  

class DeleteGroupTestCases(APITestCase):
   """delete groups test cases"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_group_delete_for_superuser(self):
      """Super user can delete the groups """
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.delete(reverse("group-detail",kwargs={"pk":self.teacher_group.id}))
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

   def test_group_delete_for_authenticate_user(self):
      """authenticate user can not delete the group """
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.delete(reverse("group-detail",kwargs={"pk":self.teacher_group.id}))
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_delete_for_teacher_user(self):
      """teacher user can not delete the group """
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.delete(reverse("group-detail",kwargs={"pk":self.teacher_group.id}))
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_delete_for_coach_user(self):
      """coach user can not delete the group """
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.delete(reverse("group-detail",kwargs={"pk":self.teacher_group.id}))
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_delete_for_anonymous_user(self):
      """Anonymous user can not delete group """
      response = self.client.delete(reverse("group-detail",kwargs={"pk":self.teacher_group.id}))
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListGroupTestCases(APITestCase):
   """list groups test cases"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_group_list_for_superuser(self):
      """super user can see groups"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("group-list"))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_group_list_for_authenticate_user(self):
      """authenticated user can see the groups """
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("group-list"))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_group_list_for_teacher_user(self):
      """Teacher user can see the groups """
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("group-list"))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_group_list_for_coach_user(self):
      """Caach user can see the groups """
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("group-list"))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_group_list_for_anonymous_user(self):
      """anonymous user can not see the groups """
      response = self.client.get(reverse("group-list"))
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class CreateSchoolTestCases(APITestCase):
   """Create schools test cases"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_school_create_by_superuser(self):
      """Super user can post the new school only """
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse("school-list"),data= {"name":"nam"})
      self.assertEqual(response.status_code, status.HTTP_201_CREATED)

   def test_school_create_by_authenticate_user(self):
      """Authenticated user can not post the new school"""
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse("school-list"),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_school_post_by_anonymous_user(self):
      """Anonymous user can not post the new school """
      response = self.client.post(reverse("school-list"),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_school_create_by_coach_user(self):
      """coach user can not post the new school"""
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse("school-list"),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_school_create_by_teacher_user(self):
      """teacher user cna not create the school"""
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse("school-list"),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)


class UpdateSchoolTestCases(APITestCase):
   """Update school test cases"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )
   def test_school_update_for_superuser(self):
      """Super user can update the schools only """
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.put(reverse("school-detail",kwargs={"pk":self.school.id}),data= {'name':'name'})
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_school_update_for_authenticate_user(self):
      """authenticate user can not update the schools"""
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.put(reverse("school-detail",kwargs={"pk":self.school.id}),data= {'name':'nam'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_school_update_for_anonymous_user(self):
      """Anonymous user can not update schools """
      response = self.client.put(reverse("school-detail",kwargs={"pk":self.school.id}),data= {'name':'nam'})
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_school_update_for_teacher_user(self):
      """Teacher user can not update the schools"""
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.put(reverse("school-detail",kwargs={"pk":self.school.id}),data= {'name':'nam'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
   def test_group_update_for_coach_user(self):
      """Coach user can not update the schools"""
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.put(reverse("school-detail",kwargs={"pk":self.school.id}),data= {'name':'nam'})
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
  

class DeleteSchoolTestCases(APITestCase):
   """delete school test cases"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_group_delete_for_superuser(self):
      """Super user can delete the school """
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.delete(reverse("school-detail",kwargs={"pk":self.school.id}))
      self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)

   def test_group_delete_for_authenticate_user(self):
      """authenticate user can not delete the school """
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.delete(reverse("school-detail",kwargs={"pk":self.school.id}))
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_delete_for_teacher_user(self):
      """teacher user can not delete the school """
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.delete(reverse("school-detail",kwargs={"pk":self.school.id}))
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_delete_for_coach_user(self):
      """coach user can not delete the school """
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.delete(reverse("school-detail",kwargs={"pk":self.school.id}))
      self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

   def test_group_delete_for_anonymous_user(self):
      """Anonymous user can not delete school """
      response = self.client.delete(reverse("school-detail",kwargs={"pk":self.school.id}))
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class ListSchoolTestCases(APITestCase):
   """list school test cases"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_school_list_for_superuser(self):
      """super user can see schools"""
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("school-list"))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_school_list_for_authenticate_user(self):
      """authenticated user can see the schools """
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("school-list"))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_school_list_for_teacher_user(self):
      """Teacher user can see the schools """
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("school-list"))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_school_list_for_coach_user(self):
      """Caach user can see the schools """
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.get(reverse("school-list"))
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_school_get_for_anonymous_user(self):
      """anonymous user can not see the schools """
      response = self.client.get(reverse("school-list"))
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class UserLoginTestCase(APITestCase):
   """Login and logout tests"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_anonymous_user_login(self):
      """User login creadentials"""
      data= {
         'username':'test',
         'email':"test.test@gmail.com",
         'password':'password'
      }
      response = self.client.post(reverse('login'),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_superuser_login(self):
      """super User login test"""
      data= {
         'username':'test',
         'email':"test.test@gmail.com",
         'password':'password'
      }
      token= Token.objects.create(user=self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse('login'),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_authenticateuser_login(self):
      """super User login test"""
      data= {
         'username':'test',
         'email':"test.test@gmail.com",
         'password':'password'
      }
      token= Token.objects.create(user=self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse('login'),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_coachuser_login(self):
      """super User login test"""
      data= {
         'username':'test',
         'email':"test.test@gmail.com",
         'password':'password'
      }
      token= Token.objects.create(user=self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse('login'),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_teacheruser_login(self):
      """super User login test"""
      data= {
         'username':'test',
         'email':"test.test@gmail.com",
         'password':'password'
      }
      token= Token.objects.create(user=self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse('login'),data=data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)


class UserLogoutTestCase(APITestCase):
   """Login and logout tests"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_anonymous_user_logout(self):
      """User login creadentials"""
      response = self.client.post(reverse('logout'),data={})
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

   def test_superuser_logout(self):
      """super User login test"""
      token= Token.objects.create(user=self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse('logout'),data={})
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_authenticateuser_logout(self):
      """super User login test"""
      token= Token.objects.create(user=self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse('logout'),data={})
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_coachuser_logout(self):
      """super User login test"""
      token= Token.objects.create(user=self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse('logout'),data={})
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_teacheruser_logout(self):
      """super User login test"""
      token= Token.objects.create(user=self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response = self.client.post(reverse('logout'),data={})
      self.assertEqual(response.status_code, status.HTTP_200_OK)



class ChangePasswordTestCases(APITestCase):
   """Password related tasks"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_change_password_superuser(self):
      """Change your password but you should have your old password"""
      data = {
         "old_password":"password",
         "password1":"change",
         "password2":"change"
      }
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.post(reverse("change-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_change_password_authenticateuser(self):
      """Change your password but you should have your old password"""
      data = {
         "old_password":"password",
         "password1":"change",
         "password2":"change"
      }
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.post(reverse("change-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_change_password_coachuser(self):
      """Change your password but you should have your old password"""
      data = {
         "old_password":"password",
         "password1":"change",
         "password2":"change"
      }
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.post(reverse("change-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_change_password_teacheruser(self):
      """Change your password but you should have your old password"""
      data = {
         "old_password":"password",
         "password1":"change",
         "password2":"change"
      }
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.post(reverse("change-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_change_password_anonymoususer(self):
      """Change your password but you should have your old password"""
      data = {
         "old_password":"password",
         "password1":"change",
         "password2":"change"
      }
      response= self.client.post(reverse("change-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


class PasswordResetSendMailTestCases(APITestCase):
   """Password related tasks"""
   def setUp(self):
      self.teacher_group = Group.objects.create(
         name= "Teacher"
      )
      self.coach_group = Group.objects.create(
         name= "Coach"
      )
      self.school = School.objects.create( 
         name= "Primary" 
      )
      self.teacher_user = User.objects.create_user( 
         username= "test",email= "test.test.1002.2001@gmail.com",
         phone_number=   "01231231230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password",school=self.school,groups=self.teacher_group
      )
      self.coach_user = User.objects.create_user( 
         username= "test1",  email= "test.test.1002.20@gmail.com",
         phone_number= "01231231000", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password",school=self.school,groups=self.coach_group
      )
      self.authenticate_user = User.objects.create_user( 
         username= "test2",email= "test.test.10.2001@gmail.com",
         phone_number=   "012331230",dob= "2022-03-02",street= "231",
         zip_code= 246285,city="Banglore",state= "Karnataka",country= "India",
         password= "password"
      )
      self.superuser = User.objects.create_superuser( 
         username= "super",email= "test.test.1002.200@gmail.com",
         phone_number= "0123123123", dob= "2022-03-02", street= "231",
         zip_code= 246285, city= "Banglore", state= "Karnataka",
         country= "India", password= "password"
      )

   def test_forgot_password_send_mail_superuser(self):
      """Forgot your password, enter your mail you will get email to reset password"""
      data = {
         'email' : "user@gmail.com",
      }
      token = Token.objects.create(user = self.superuser)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.post(reverse("reset-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)
   
   def test_forgot_password_send_mail_authenticate(self):
      """Forgot your password, enter your mail you will get email to reset password"""
      data = {
         'email' : "user@gmail.com",
      }
      token = Token.objects.create(user = self.authenticate_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.post(reverse("reset-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_forgot_password_send_mail_coach(self):
      """Forgot your password, enter your mail you will get email to reset password"""
      data = {
         'email' : "user@gmail.com",
      }
      token = Token.objects.create(user = self.coach_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.post(reverse("reset-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_forgot_password_send_mail_teacher(self):
      """Forgot your password, enter your mail you will get email to reset password"""
      data = {
         'email' : "user@gmail.com",
      }
      token = Token.objects.create(user = self.teacher_user)
      self.client.credentials(HTTP_AUTHORIZATION='Token ' + token.key)
      response= self.client.post(reverse("reset-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)

   def test_forgot_password_send_mail_unauthenticate(self):
      """Forgot your password, enter your mail you will get email to reset password"""
      data = {
         'email' : "user@gmail.com",
      }
      response= self.client.post(reverse("reset-password"), data= data)
      self.assertEqual(response.status_code, status.HTTP_200_OK)






