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
from homeworks.views import CreateHomeworkAPI

from rest_framework.test import APIRequestFactory

# Create your tests here.

class HomeworkTest(TestCase):
    #check url
    def test_create_url(self):
        url = reverse('createHomework')
        self.assertEquals(resolve(url).func.view_class, CreateHomeworkAPI)

    #succesfully create a Homework
