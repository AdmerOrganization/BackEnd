from django import forms
from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.fields import CharField
from .models import classroom
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators

class Classroom_CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = classroom
        fields = ('id', 'password' , 'classroom_token', 'title', 'avatar', 'teacher_name', 'description', 'limit' , 'teacher_id')
        extra_kwargs = {
            'classroom_token': {'read_only': True, 'required':False},
            'id': {'read_only': True, 'required':False},
            'password': {'required':True, 'write_only':True},
        }
    def validate_password(self, data):
            validators.validate_password(password=data, user=User)
            return data
    def create(self, validated_data):
        validated_data['password'] = make_password(validated_data.get('password'))
        return super(Classroom_CreateSerializer, self).create(validated_data)


class Classroom_SearchSerializer(serializers.ModelSerializer):
    class Meta:
        model = classroom
        fields = ('id', 'classroom_token', 'title','teacher_name', 'time')
        extra_kwargs = {
            'classroom_token': {'read_only': True, 'required':False},
            'id': {'read_only': True, 'required':False},
            'title': {'required':False},
            'teacher_name': {'required':False},
            'time': {'required':False},
        }