from audioop import reverse
from django.test import TestCase,TransactionTestCase

from channels.testing import HttpCommunicator,ApplicationCommunicator,WebsocketCommunicator
from channels.routing import URLRouter
from .consumers import ChatConsumer
from accounts.models import User
from classes.models import classroom
from datetime import datetime
from django.urls import resolve, reverse
from rest_framework import generics, status
import json
from rest_framework.test import APIClient
from asgiref.sync import sync_to_async
from channels.db import database_sync_to_async
from django import db
from django.urls import re_path
from . import consumers

communicator = ApplicationCommunicator(ChatConsumer, {"type": "http"})

class MyTests(TransactionTestCase):
    #succesfully create a user
    @database_sync_to_async
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
    @database_sync_to_async
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

    def test_connect(self):
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


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)

        response = client.get(reverse('room', kwargs={'id':selectclass.id}))
        self.assertEqual(response.status_code, status.HTTP_200_OK)
    

    def test_connect_fail_wrong_classroom(self):
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


        client = APIClient()
        client.credentials(HTTP_AUTHORIZATION='Token ' + user_token)

        response = client.get(reverse('room', kwargs={'id':selectclass.id + 1}))
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
    
    async def test_my_consumer(self):
        application = URLRouter([
            re_path(r'testws/(?P<room_name>[0-9A-Za-z_\-]{1,32})/$', consumers.ChatConsumer.as_asgi()),
        ])
        user_token = await self.user_generate()
        class_token = await self.class_generate(user_token)
        db.connections.close_all()
        headers = [(b'origin', b'...'), (b'cookie', self.client.cookies.output(header='Authorization=' + user_token + "Classroom=" + class_token + '; path=/''', sep='; ').encode())]
        communicator = WebsocketCommunicator(application, "/testws/"+class_token+'/', headers)
        await communicator.connect()
        await communicator.send_input({
            "type": "chat_message",
            "message": "hello",
            "fname": "mr",
            "lname": "tester",
            "id": 3,
            "token": class_token,
            "timestamp": "2:15-2022/24/05",
            "user_token": user_token,
        })
        assert await communicator.receive_nothing(timeout=0.5) is False
        event = await communicator.receive_output(timeout=0.5)

        assert event["type"] == "websocket.send"
        await communicator.disconnect()
    
    async def test_my_consumer_nothing(self):
        communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "chat/testws/")
        assert await communicator.receive_nothing(timeout=0.5) is True

    async def test_my_consumer_fail_no_class_token(self):
        
        user_token = await self.user_generate()
        class_token = await self.class_generate(user_token)
        db.connections.close_all()
        headers = [(b'origin', b'...'), (b'cookie', self.client.cookies.output(header='Authorization=' + user_token + "Classroom=" + class_token + '; path=/''', sep='; ').encode())]
        try:
            communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "chat/testws/", headers)
            respone = await communicator.send_input({
                "type": "chat_message",
                "message": "hello",
                "fname": "mr",
                "lname": "tester",
                "id": 3,
                #"token": class_token,
                "timestamp": "2:15-2022/24/05",
                "user_token": user_token,
            })
            event = await communicator.receive_output(timeout=0.5)
        except Exception as e:
            assert e.args == ('no class token_exception',)

    async def test_my_consumer_fail_no_message(self):
        
        user_token = await self.user_generate()
        class_token = await self.class_generate(user_token)
        db.connections.close_all()
        headers = [(b'origin', b'...'), (b'cookie', self.client.cookies.output(header='Authorization=' + user_token + "Classroom=" + class_token + '; path=/''', sep='; ').encode())]
        try:
            communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "chat/testws/", headers)
            respone = await communicator.send_input({
                "type": "chat_message",
                #"message": "hello",
                "fname": "mr",
                "lname": "tester",
                "id": 3,
                "token": class_token,
                "timestamp": "2:15-2022/24/05",
                "user_token": user_token,
            })
            event = await communicator.receive_output(timeout=0.5)
        except Exception as e:
            assert e.args == ('no message_exception',)
        
    async def test_my_consumer_fail_no_fname(self):
        
        user_token = await self.user_generate()
        class_token = await self.class_generate(user_token)
        db.connections.close_all()
        headers = [(b'origin', b'...'), (b'cookie', self.client.cookies.output(header='Authorization=' + user_token + "Classroom=" + class_token + '; path=/''', sep='; ').encode())]
        try:
            communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "chat/testws/", headers)
            respone = await communicator.send_input({
                "type": "chat_message",
                "message": "hello",
                #"fname": "mr",
                "lname": "tester",
                "id": 3,
                "token": class_token,
                "timestamp": "2:15-2022/24/05",
                "user_token": user_token,
            })
            event = await communicator.receive_output(timeout=0.5)
        except Exception as e:
            assert e.args == ('no fname_exception',)

    async def test_my_consumer_fail_no_lname(self):
        
        user_token = await self.user_generate()
        class_token = await self.class_generate(user_token)
        db.connections.close_all()
        headers = [(b'origin', b'...'), (b'cookie', self.client.cookies.output(header='Authorization=' + user_token + "Classroom=" + class_token + '; path=/''', sep='; ').encode())]
        try:
            communicator = WebsocketCommunicator(ChatConsumer.as_asgi(), "chat/testws/", headers)
            respone = await communicator.send_input({
                "type": "chat_message",
                "message": "hello",
                "fname": "mr",
                #"lname": "tester",
                "id": 3,
                "token": class_token,
                "timestamp": "2:15-2022/24/05",
                "user_token": user_token,
            })
            event = await communicator.receive_output(timeout=0.5)
        except Exception as e:
            assert e.args == ('no lname_exception',)
