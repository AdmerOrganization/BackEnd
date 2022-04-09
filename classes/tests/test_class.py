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
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('create'), payload)
        print (response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        
    
    