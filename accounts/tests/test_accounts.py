import imp
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.core import mail
import time
from rest_framework.test import APIRequestFactory
from django.test import Client

class AccountTest(TestCase):

    def test_signup(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'Bass@567',
            'password2': 'Bass@567',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_signin(self):
        signup_data = {
            'email': 'test@gmail.com',
            'password': 'Bass@567',
            'password2': 'Bass@567',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
        }
        response = self.client.post(reverse('signup'), signup_data)

        user =  User.objects.get(email='test@gmail.com')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        signin_data = {
            'username': 'test1',
            'password': 'Bass@567',
        }
        response = self.client.post(reverse('signin'), signin_data)
        print(response)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_reset_password(self):
        data_signup = {
            'email': 'test@gmail.com',
            'password': 'Bass@567',
            'password2': 'Bass@567',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
        }
        response = self.client.post(reverse('signup'), data_signup)

        data_reset = {
            'email': 'test@gmail.com',
        }

        response = self.client.post('/password-reset/', data_reset)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

        # self.user = User.objects.get(email='test@gmail.com')
        time.sleep(0.1)
        url = mail.outbox[0].body
        token = url.split("?tok",1)[1] 

        data_verify = {
            'email': 'test@gmail.com',
            'token': str(token),
        }

        response = self.client.post('password-reset/confirm', data_verify)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
