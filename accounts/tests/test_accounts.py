import imp
from django.test import TestCase
from django.urls import reverse
from rest_framework import status
from django.contrib.auth.models import User
from django.core import mail
import time
from rest_framework.test import APIRequestFactory
from django.test import Client
from rest_framework.test import APIClient
import json

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

    def test_signup_fail_same_email(self):
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

        data = {
            'email': 'test@gmail.com',
            'password': 'Bass@567',
            'password2': 'Bass@567',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_password_missmathch(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'Bass@567',
            'password2': 'Bass@5671',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_password_short(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'Bass@56',
            'password2': 'Bass@56',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_password_no_number(self):
        data = {
            'email': 'test@gmail.com',
            'password': 'Bass@aaa',
            'password2': 'Bass@aaa',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_signup_fail_password_no_letter(self):
        data = {
            'email': 'test@gmail.com',
            'password': '12312$13',
            'password2': '12312$13',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    

    def test_signup_fail_no_fname(self):
        data = {
            'email': 'test@gmail.com',
            'password': '12312$13',
            'password2': '12312$13',
            'username': 'test1',
            'first_name': '',
            'last_name': 'Robinson',
        }
        response = self.client.post(reverse('signup'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


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
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_signin_fail(self):
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

        signin_data = {
            'username': 'test1',
            'password': 'Bass@567',
        }
        response = self.client.post(reverse('signin'), signin_data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

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

    def test_edit(self):
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
        user =  User.objects.get(username='test1')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'Bass@567',
            'username': 'test1',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            'email': 'test@gmail.com',
            'password': 'Bass@567',
            'password2': 'Bass@567',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
            'phone_number': '091200000000',
        }
        response = client.put(reverse('edit-profile'),data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_edit_fail(self):
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
        user =  User.objects.get(username='test1')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'Bass@567',
            'username': 'test1',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        data = {
            'email': 'test@gmail.com',
            'password': 'Bass@567',
            'password2': 'Bass@567',
            'username': 'test1',
            'first_name': 'James',
            'last_name': 'Robinson',
            'phone_number': '09120000000000',
        }
        response = client.put(reverse('edit-profile'),data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)


    def test_current_user(self):
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
        user =  User.objects.get(username='test1')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        payload = {
            'password': 'Bass@567',
            'username': 'test1',
        }
        response = self.client.post(reverse('signin'), payload)
        items = json.loads(response.content)
        token = items ['token']
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.post(reverse('current-user'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)