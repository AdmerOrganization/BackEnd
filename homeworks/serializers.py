from turtle import home
from rest_framework import serializers
from django.contrib.auth.models import User

from classes.models import classroom
from classes.serializers import Classroom_GetSerializer
from .models import homework
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators


class Homework_CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = homework
        fields = ('id', 'homework_token', 'title', 'file',
                  'deadline' , 'classroom')
        extra_kwargs = {
            'homework_token': {'read_only': True, 'required': False},
            'id': {'read_only': True, 'required': False},
        }




