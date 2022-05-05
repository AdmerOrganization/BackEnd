
import json
from rest_framework.test import RequestsClient
from rest_framework.test import APIClient
import time
from django.test import TestCase
from django.urls import resolve, reverse
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.views import EditAPI
from accounts.models import User
from rest_framework import generics, status
from rest_framework import serializers

from datetime import datetime
from homeworks.models import homework
from homeworks.views import CreateHomeworkAPI
from classes.models import classroom

from rest_framework.test import APIRequestFactory

from django.core.files.uploadedfile import SimpleUploadedFile
# Create your tests here.

class HomeworkTest(TestCase):
    #check url
    def test_create_url(self):
        url = reverse('createHomework')
        self.assertEquals(resolve(url).func.view_class, CreateHomeworkAPI)

    #succesfully create a Homework

    def user_generate(self):
        # Create account
        payload = {
            'email': 'testemail@gmail.com',
            'password': 'Pass@12345',
            'password2': 'Pass@12345',
            'username': 'test_user',
            'first_name': 'testName',
            'last_name': 'testLName',
        }
        
        response = self.client.post(reverse('signup'), payload)
        user =  User.objects.get(username='test_user')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'Pass@12345',
            'username': 'test_user',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        user_token = items ['token']
        return user_token

    def user_generate2(self):
        # Create account
        payload = {
            'email': 'testemail2@gmail.com',
            'password': 'Pass@12345',
            'password2': 'Pass@12345',
            'username': 'test_user2',
            'first_name': 'testName',
            'last_name': 'testLName',
        }
        
        response = self.client.post(reverse('signup'), payload)
        user =  User.objects.get(username='test_user2')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'Pass@12345',
            'username': 'test_user2',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        user_token = items ['token']
        return user_token

    def class_generate(self, user_token):
        # Create class

        payload = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('create'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        selectclass = classroom.objects.get(title = "Class Test")
        class_token = selectclass.classroom_token

        return class_token


    def generate_file(self):

        f = open( 'some_file.txt', 'w+')
        f.write("text")
            
        return f


    #HOMEWORK CREATE ------------------------------------------------------------------------------------------------------

    def test_create_homework(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_create_fail_with_deadline(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '',
            'description': 'this is a test class',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_fail_with_deadline_overflow(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/05/05-08:08 ----------------------------------------------------------------------------------------------',
            'description': 'this is a test class',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_fail_with_title(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': '',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    
    def test_create_fail_with_title_overflow(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework title is something larger than 100 characters-----------------------------------------------',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_fail_with_description(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': '',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_fail_with_classroom(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'classroom': ''
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_classroom_not_exist(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'classroom': 100
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_file(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': file,
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_create_fail_with_user_token(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token +'#')
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)


    def test_create_fail_with_user_is_not_teacher(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        user_token = self.user_generate2()
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)

    #HOMEWORK EDIT ------------------------------------------------------------------------------------------------------

    def homework_generate(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        file = self.generate_file()
        selectclass = classroom.objects.get(classroom_token = class_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'classroom': selectclass.id
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('createHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        selecthomework = homework.objects.get(title = 'homework_test')
        return selecthomework.homework_token

    def test_edit_homework(self):
        user_token = self.user_generate()
        homework_token = self.homework_generate()
        file = self.generate_file()
        selecthomework = homework.objects.get(homework_token = homework_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'homework_token': selecthomework.homework_token
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('editHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_fail_with_wrong_homework_token(self):
        user_token = self.user_generate()
        homework_token = self.homework_generate()
        file = self.generate_file()
        selecthomework = homework.objects.get(homework_token = homework_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'homework_token': selecthomework.homework_token +'.'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('editHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_fail_with_no_homework_token(self):
        user_token = self.user_generate()
        homework_token = self.homework_generate()
        file = self.generate_file()
        selecthomework = homework.objects.get(homework_token = homework_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'homework_token': ''
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('editHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_edit_fail_with_wrong_token(self):
        user_token = self.user_generate()
        homework_token = self.homework_generate()
        file = self.generate_file()
        selecthomework = homework.objects.get(homework_token = homework_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'homework_token': selecthomework.homework_token
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token + '1')
        response = client.post(reverse('editHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_edit_fail_with_user_is_not_teacher(self):
        user_token = self.user_generate()
        homework_token = self.homework_generate()
        user_token = self.user_generate2()
        file = self.generate_file()
        selecthomework = homework.objects.get(homework_token = homework_token)
        payload = {
            'file': '',
            'title': 'homework_test',
            'deadline': '2022/4/12-08:08',
            'description': 'this is a test class',
            'homework_token': selecthomework.homework_token
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('editHomework'), payload)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)