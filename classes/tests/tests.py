from django.test import TestCase
from django.urls import resolve, reverse
from classes.tests import test_class
from classes.views import Classroom_SearchAPI, Classroom_DeleteSerializer, Classroom_EditSerializer, Classroom_GetSerializer
from rest_framework.test import APIClient
from rest_framework import generics, status
from accounts.models import User
import json
from classes.models import classroom
# from classes.tests.test_class import clas


class TestClass(TestCase):

    def token_generate(self):
        # Create account
        data = {
            'email': 'testemail@gmail.com',
            'password': 'Pass@12345',
            'password2': 'Pass@12345',
            'username': 'test_user',
            'first_name': 'testName',
            'last_name': 'testLName',
        }
        
        response = self.client.post(reverse('signup'), data)
        user =  User.objects.get(username='test_user')
        profile = user.userprofile
        profile.is_verified = True
        profile.save()

        # Login
        data = {
            'password': 'Pass@12345',
            'username': 'test_user',
        }
        response = self.client.post(reverse('signin'), data)
        items = json.loads(response.content)
        token = items ['token']
        return token
    
    def create_class(self, token):

        data = {
            'title': 'Class Test',
            'teacher_name': 'mr test',
            'limit': 12,
            'description': 'this is a test class',
            'password' : '1234Test'
        }
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        client.post(reverse('create'), data)

    def test_classrooms_getall(self):
        token = self.token_generate()
        self.create_class(token)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('get-all'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_classrooms_get_specific(self):
        token = self.token_generate()
        self.create_class(token)
        self.create_class(token)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('list-class-by-id' ,kwargs={'pk':2}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_classrooms_get_created(self):
        token = self.token_generate()
        self.create_class(token)
        self.create_class(token)

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('get-created'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    
    def test_classrooms_edit(self):
        token = self.token_generate()
        self.create_class(token)
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        response = client.get(reverse('get-all'))
        classroom_token = response.data[0]['classroom_token']

        initial_title = response.data[0]['title']

        data = {
            'title': 'New Title',
            'classroom_token': str(classroom_token),
        }

        response = client.put(reverse('editClass'), data)

        response = client.get(reverse('get-all'))
        secondary_title = response.data[0]['title']

        self.assertNotEqual(initial_title, secondary_title)

    def test_classrooms_delete(self):
        token = self.token_generate()
        self.create_class(token)
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('get-all'))
        classroom_token = response.data[0]['classroom_token']

        data = {
            'classroom_token': str(classroom_token),
        }

        response = client.delete(reverse('delete'), data)
        classes = classroom.objects.filter(classroom_token = str(classroom_token)).count()
        
        is_deleted = True if classes == 0 else False

        self.assertTrue(is_deleted)

    def test_classrooms_delete_fail(self):
        token = self.token_generate()
        self.create_class(token)
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('get-all'))
        classroom_token = response.data[0]['classroom_token']

        data = {
            'classroom_token': str(classroom_token)+'1',
        }

        response = client.delete(reverse('delete'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_classrooms_delete_fail_no_token(self):
        token = self.token_generate()
        self.create_class(token)
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('get-all'))
        classroom_token = response.data[0]['classroom_token']

        data = {
            'classroom_token': '',
        }

        response = client.delete(reverse('delete'), data)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)

    def test_classrooms_delete_not_valid(self):
        token = self.token_generate()
        self.create_class(token)
        client = APIClient()

        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('get-all'))
        classroom_token = response.data[0]['classroom_token']


        response = client.delete(reverse('delete'))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)



    def test_classrooms_search(self):
        token = self.token_generate()
        self.create_class(token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        data = {
            'title': 'Class Test',
            'teacher_name': 'mr ahmadi',
            'time': '1400',
        }

        response = client.post(reverse('search'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_classrooms_search2(self):
        token = self.token_generate()
        self.create_class(token)


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)


        response = client.post(reverse('search'))
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_classrooms_search_token(self):
        token = self.token_generate()
        self.create_class(token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('get-all'))
        classroom_token = response.data[0]['classroom_token']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        data = {
            'classroom_token': classroom_token,

        }

        response = client.post(reverse('search'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_classrooms_search_token_fail(self):
        token = self.token_generate()
        self.create_class(token)
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)
        response = client.get(reverse('get-all'))
        classroom_token = response.data[0]['classroom_token']

        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + token)

        data = {
            'classroom_token': classroom_token+'ad',

        }

        response = client.post(reverse('search'), data)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
