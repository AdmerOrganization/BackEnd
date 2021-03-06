from rest_framework import serializers
from django.contrib.auth.models import User

from classes.models import classroom
from classes.serializers import Classroom_GetSerializer
from .models import answer, homework
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators


class Homework_CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = homework
        fields = ('id', 'homework_token', 'title', 'description', 'file',
                  'deadline' , 'classroom')
        extra_kwargs = {
            'homework_token': {'read_only': True, 'required': False},
            'id': {'read_only': True, 'required': False},
        }



class Homework_EditSerializer(serializers.ModelSerializer):

    class Meta:
        model = homework
        fields = ('id', 'homework_token', 'title', 'description', 'file',
                  'deadline' , 'classroom')
        extra_kwargs = {
            'homework_token': {'required': True},
            'classroom': {'read_only': True, 'required': False},
            'id': {'read_only': True, 'required': False},
            'title': {'required': False},
            'deadline': {'required': False},
            'description': {'required': False},
            'file': {'required': False},
        }

class Homework_DisplaySerializer(serializers.ModelSerializer):

    class Meta:
        model = homework
        fields = ('id', 'homework_token', 'title', 'description', 'file',
                  'deadline' , 'classroom')
        extra_kwargs = {
            'homework_token': {'required': True},
            'classroom': {'read_only': True, 'required': False},
            'id': {'read_only': True, 'required': False},
            'title': {'read_only': True,'required': False},
            'deadline': {'read_only': True,'required': False},
            'description': {'read_only': True,'required': False},
            'file': {'read_only': True,'required': False},
        }

class Homework_ListSerializer(serializers.ModelSerializer):

    class Meta:
        model = homework
        fields = ('id', 'homework_token', 'title',
                  'deadline' , 'classroom')
        extra_kwargs = {
            'homework_token': {'read_only': True , 'required': False},
            'classroom': {'required': True},
            'id': {'read_only': True, 'required': False},
            'title': {'read_only': True,'required': False},
            'deadline': {'read_only': True,'required': False},
            'description': {'read_only': True,'required': False},
            'file': {'read_only': True,'required': False},
        }


class Answer_CreateSerializer(serializers.ModelSerializer):

    class Meta:
        model = answer
        fields = ('id', 'homework', 'file', 'user')
        extra_kwargs = {
            'homework': {'required': True},
            'id': {'read_only': True, 'required': False},
            'user': {'read_only': True, 'required': False},
        }

class UserSerializer(serializers.ModelSerializer):

    class Meta:
        model = User
        fields = ('id', 'username', 'first_name', 'last_name')
        extra_kwargs = {
            'id': {'read_only': True, 'required': False},
        }

class Answer_ListSerializer(serializers.ModelSerializer):
    user = UserSerializer( read_only=True)
    class Meta:
        model = answer
        fields = ('id', 'homework', 'file', 'user', 'date')
        extra_kwargs = {
            'homework': {'required': True},
            'id': {'read_only': True, 'required': False},
            'user': {'read_only': True, 'required': False},
            'date': {'read_only': True, 'required': False},
            'file': {'read_only': True, 'required': False},
        }
