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
from rest_framework import generics, status
from rest_framework import serializers

from datetime import datetime
from classes.views import CreateClassAPI

from rest_framework.test import APIRequestFactory

# Create your tests here.

class ClassTest(TestCase):
    #check url
    def test_create_url(self):
        url = reverse('create')
        self.assertEquals(resolve(url).func.view_class, CreateClassAPI)


    #succesfully create a class
    def test_create(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

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
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    #check for mail
    def test_create_email(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

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
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        time.sleep(0.1)
        self.assertEqual(len(mail.outbox), 2)


    #fail senarios 
    def test_create_fail_with_title(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': '',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    def test_create_fail_with_title_overflow(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'a title that is longer than 100 characters/////////////////////////////////////////////////////////////////////////////////////',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_teacher(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': '',
            'limit': 12,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    
    def test_create_fail_with_teacher_overflow(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': 'a name that is longer than 100 characters/////////////////////////////////////////////////////////////////////////////////////',
            'limit': 12,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_limit(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': 'mr test',
            'limit': '',
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_limit_string(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': 'mr test',
            'limit': 'string instead of int',
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_description(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': '',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_password_lessthan8(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : ''
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_password_numeric(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : '12345678'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_password_common(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : 'aaaaaaaa'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_create_fail_with_wrong_token(self):

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
        print (response.content)
        items = json.loads(response.content)
        token = items ['token']
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        print (token)

        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token + '1')
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)

    def test_create_fail_with_no_token(self):
        # Create class

        payload = {
            'title': 'Class test',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : 'aaaaaaaa'
        }
        client = APIClient()
        #client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_401_UNAUTHORIZED)