import email
import imp
import time
from unittest import mock
from django.conf import settings
from django.core import mail
from django.test import TestCase
from django.urls import resolve, reverse
import jwt
from rest_framework_simplejwt.tokens import RefreshToken
from accounts.views import EditAPI
from accounts.models import User
from rest_framework import generics, status
from rest_framework import serializers

from datetime import datetime
from accounts.views import VerifyEmail


# Create your tests here.

class AccountTest(TestCase):
    
    def test_edit_profile(self):
        url = reverse('edit-profile')
        self.assertEquals(resolve(url).func.view_class, EditAPI)


    def test_verify_email_succeed(self):
        payload = {
            'email': 'testverifyemailsucceed@gmail.com',
            'password': 'TestpassUltra1',
            'password2': 'TestpassUltra1',
            'username': 'userTest1',
            'first_name': 'test',
            'last_name': 'test',
        }
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user = User.objects.get(email='testverifyemailsucceed@gmail.com')
        time.sleep(0.1)
        url = mail.outbox[0].body
        #print (url)
        token = url.split("?token=",1)[1]
        token = token.split(" target=",1)[0]


        # Verify 
        response = self.client.get(reverse('email-verify'), {'token': token})
        #print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_verify_email_wrong_token(self):
        payload = {
            'email': 'testverifyemailfail1@gmail.com',
            'password': 'TestpassUltra2',
            'password2': 'TestpassUltra2',
            'username': 'userTest2',
            'first_name': 'test',
            'last_name': 'test',
        }
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user = User.objects.get(email='testverifyemailfail1@gmail.com')
        time.sleep(0.1)
        url = mail.outbox[0].body
        #print (url)
        token = url.split("?token=",1)[1]
        token = token.split(" target=",1)[0]


        # Verify 
        response = self.client.get(reverse('email-verify'), {'token': token + "x"})
        #print(response.content)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"error":"Invalid token"}')

    #@mock.patch('accounts.views.datetime')
    def test_token_expiry_refresh(self):
        payload = {
            'email': 'testverifyemailfail2@gmail.com',
            'password': 'TestpassUltra3',
            'password2': 'TestpassUltra3',
            'username': 'userTest3',
            'first_name': 'test',
            'last_name': 'test',
        }
        response = self.client.post(reverse('signup'), payload)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.user = User.objects.get(email='testverifyemailfail2@gmail.com')
        time.sleep(0.1)
        url = mail.outbox[0].body
        token = url.split("?token=",1)[1]
        token = token.split(" target=",1)[0]
        payload = jwt.decode(token, settings.SECRET_KEY, 'HS256')
        payload['exp'] = 1
        token = jwt.encode(payload, settings.SECRET_KEY, algorithm='HS256')
        #today_mock.return_value = datetime(2030, 1, 1)
        response = self.client.get(reverse('email-verify'), {'token': token})
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.content, b'{"error":"Activation Expired"}')