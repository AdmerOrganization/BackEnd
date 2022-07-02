from array import array
from datetime import datetime, timedelta
from django.test import TestCase
from django.urls import resolve, reverse
from classes.tests import test_class
from classes.views import Classroom_SearchAPI, Classroom_DeleteSerializer, Classroom_EditSerializer, Classroom_GetSerializer
from rest_framework.test import APIClient
from rest_framework import generics, status
from accounts.models import User
import json
from classes.models import classroom

# Create your tests here.
class eXAMTest(TestCase):

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

    def test_exam_create(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exam_get(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.get(reverse('ExamCreateAPI'))


    def test_exam_edit(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'id': 1,
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
        response = client.put(reverse('ExamEditAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


    def test_exam_retrieve(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'id': 1,
        }
        response = client.post(reverse('ExamRetrieveAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exam_retrieve_no_id(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'classroom': selectclass.id,
            
        }
        response = client.post(reverse('ExamRetrieveAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exam_retrieve_data(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'exam_info': 1,
            'question_num': '1'

            
        }
        response = client.post(reverse('ExamDataRetrieveAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exam_retrieve_data_fail(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'exam_info': 12,
            'question_num': '1'

            
        }
        #response = client.post(reverse('ExamDataRetrieveAPI'), payload , format="json")
        #self.assertEqual(response.content, b'"Question doesn\'t exist"')


    def test_exam_start_answer(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'exam_info': 1,
        }
        response = client.post(reverse('ExamStartAnsweringAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        response = client.post(reverse('ExamStartAnsweringAPI'), payload , format="json")
        self.assertEqual(response.content, b'"Exam already started"')

    def test_exam_finish_answer(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'exam_info': 1,
        }
        response = client.post(reverse('ExamFinishAnsweringAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(reverse('ExamStartAnsweringAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(reverse('ExamFinishAnsweringAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(reverse('ExamFinishAnsweringAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

    def test_exam_answer(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'exam_info': 1,
            'answers':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]

        }
        response = client.post(reverse('ExamAnswersAPI'), payload , format="json")
        self.assertEqual(response.content, b'"You have to start the exam first"')


        payload = {
            'exam_info': 1,
        }

        response = client.post(reverse('ExamStartAnsweringAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)


        payload = {
            'exam_info': 1,
            'answers':[
                ['gozine1','gozine2']
            ]

        }
        response = client.post(reverse('ExamAnswersAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        response = client.post(reverse('ExamAnswersAPI'), payload , format="json")
        self.assertEqual(response.content, b'"User has already answered this exam"')




        payload = {
            'exam_info': 1,
        }
        response = client.post(reverse('ExamFinishAnsweringAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'exam_info': 1,
            'answers':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]

        }
        response = client.post(reverse('ExamAnswersAPI'), payload , format="json")
        self.assertEqual(response.content, b'"User has already finished this exam"')





    def test_exam_calculate_fail(self):
        user_token = self.user_generate()
        class_token = self.class_generate(user_token)
        selectclass = classroom.objects.get(classroom_token = class_token)
        user = selectclass.teacher
        payload = {
            'creator': user.id,
            'classroom': selectclass.id,
            'name': 'quiz1',
            'questions_count': 1,
            'start_time': datetime.now(),
            'finish_time': (datetime.now() + timedelta(hours=1)),
            'data':[
                ['1','soale1','gozine1','gozine2','gozine3','gozine3',2]
            ]
            
        }
    
        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)
        response = client.post(reverse('ExamCreateAPI'), payload , format="json")
        self.assertEqual(response.status_code, status.HTTP_200_OK)

        payload = {
            'exam_info': 1,
        }
        response = client.post(reverse('ExamCalculateResultAPI'), payload , format="json")
        self.assertEqual(response.content, b'"You have to finish the exam first"')

