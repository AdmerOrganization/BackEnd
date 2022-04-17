import email
import imp
import json
from rest_framework.test import RequestsClient
from rest_framework.test import APIClient
import time
from unittest import mock
from django.conf import settings
from django.core import mail
from django.db import connection
from django.test import TestCase
from django.test import Client
from django.urls import resolve, reverse
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.views import EditAPI
from accounts.models import User
from classes.models import classroom

from rest_framework import generics, status
from rest_framework import serializers

from datetime import datetime
from classes.views import JoinClassAPI

from rest_framework.test import APIRequestFactory

# Create your tests here.

class ClassTest(TestCase):
    #check url
    def test_create_url(self):
        url = reverse('join')
        self.assertEquals(resolve(url).func.view_class, JoinClassAPI)


    #succesfully join a class
    def test_join(self):

        # Create account
        payload = {
            'email': 'testCreateClass1@gmail.com',
            'password': 'TestpassUltra2',
            'password2': 'TestpassUltra2',
            'username': 'userTest2',
            'first_name': 'test',
            'last_name': 'test',
        }
        
    
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user =  User.objects.get(email='testCreateClass1@gmail.com')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'TestpassUltra2',
            'username': 'userTest2',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create class

        payload = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # join a class

        selectclass = classroom.objects.all().first()
        payload = {
            'classroom_token' : selectclass.classroom_token,
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('join'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    #failed scenarios
    def test_join_no_space(self):

        # Create account
        payload = {
            'email': 'testCreateClass1@gmail.com',
            'password': 'TestpassUltra2',
            'password2': 'TestpassUltra2',
            'username': 'userTest2',
            'first_name': 'test',
            'last_name': 'test',
        }
        
    
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user =  User.objects.get(email='testCreateClass1@gmail.com')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'TestpassUltra2',
            'username': 'userTest2',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create class

        payload = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 3,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # join a class

        selectclass = classroom.objects.all().first()
        selectclass.filled = 3
        selectclass.save()
        payload = {
            'classroom_token' : selectclass.classroom_token,
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('join'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_join_no_user_token(self):

        # Create account
        payload = {
            'email': 'testCreateClass1@gmail.com',
            'password': 'TestpassUltra2',
            'password2': 'TestpassUltra2',
            'username': 'userTest2',
            'first_name': 'test',
            'last_name': 'test',
        }
        
    
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user =  User.objects.get(email='testCreateClass1@gmail.com')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'TestpassUltra2',
            'username': 'userTest2',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create class

        payload = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 3,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # join a class

        selectclass = classroom.objects.all().first()
        payload = {
            'classroom_token' : selectclass.classroom_token,
            'password' : '1234Test'
        }
        client = APIClient()
        response = client.post(reverse('join'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_join_wrong_password(self):

        # Create account
        payload = {
            'email': 'testCreateClass1@gmail.com',
            'password': 'TestpassUltra2',
            'password2': 'TestpassUltra2',
            'username': 'userTest2',
            'first_name': 'test',
            'last_name': 'test',
        }
        
    
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user =  User.objects.get(email='testCreateClass1@gmail.com')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'TestpassUltra2',
            'username': 'userTest2',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create class

        payload = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 3,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # join a class

        selectclass = classroom.objects.all().first()
        payload = {
            'classroom_token' : selectclass.classroom_token,
            'password' : '1234Test_somethingwrong'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('join'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_join_no_password(self):

        # Create account
        payload = {
            'email': 'testCreateClass1@gmail.com',
            'password': 'TestpassUltra2',
            'password2': 'TestpassUltra2',
            'username': 'userTest2',
            'first_name': 'test',
            'last_name': 'test',
        }
        
    
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user =  User.objects.get(email='testCreateClass1@gmail.com')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'TestpassUltra2',
            'username': 'userTest2',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create class

        payload = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 3,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # join a class

        selectclass = classroom.objects.all().first()
        payload = {
            'classroom_token' : selectclass.classroom_token,
            'password' : ''
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('join'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_join_wrong_class_token(self):

        # Create account
        payload = {
            'email': 'testCreateClass1@gmail.com',
            'password': 'TestpassUltra2',
            'password2': 'TestpassUltra2',
            'username': 'userTest2',
            'first_name': 'test',
            'last_name': 'test',
        }
        
    
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user =  User.objects.get(email='testCreateClass1@gmail.com')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'TestpassUltra2',
            'username': 'userTest2',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create class

        payload = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 3,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # join a class

        selectclass = classroom.objects.all().first()
        payload = {
            'classroom_token' : selectclass.classroom_token + "sth",
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('join'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
   
    def test_join_no_class_token(self):

        # Create account
        payload = {
            'email': 'testCreateClass1@gmail.com',
            'password': 'TestpassUltra2',
            'password2': 'TestpassUltra2',
            'username': 'userTest2',
            'first_name': 'test',
            'last_name': 'test',
        }
        
    
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user =  User.objects.get(email='testCreateClass1@gmail.com')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'TestpassUltra2',
            'username': 'userTest2',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create class

        payload = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 3,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # join a class

        selectclass = classroom.objects.all().first()
        payload = {
            'classroom_token' : '',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('join'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_join_user_already_joined(self):

        # Create account
        payload = {
            'email': 'testCreateClass1@gmail.com',
            'password': 'TestpassUltra2',
            'password2': 'TestpassUltra2',
            'username': 'userTest2',
            'first_name': 'test',
            'last_name': 'test',
        }
        
    
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        user =  User.objects.get(email='testCreateClass1@gmail.com')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'TestpassUltra2',
            'username': 'userTest2',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # Create class

        payload = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 3,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # join a class

        selectclass = classroom.objects.all().first()
        payload = {
            'classroom_token' : selectclass.classroom_token,
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('join'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        # join a class again

        selectclass = classroom.objects.all().first()
        payload = {
            'classroom_token' : selectclass.classroom_token,
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('join'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
      