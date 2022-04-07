from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.fields import CharField
from models import classroom

class Classroom_SearchSerializer(serializers.ModelSerializer):

    class Meta:
        model = classroom
        fields = ('id', 'classroom_token', 'avatar', 'teacher_name', 'description', 'limit',
         'time', 'teacher')
        extra_kwargs = {
            'classroom_token': {'read_only': True, 'required':False},
            'id': {'read_only': True, 'required':False},
            'avatar': {'avatar':False},
            'title': {'title':False},
            'teacher_name': {'required':False},
            'description': {'required':False},
            'limit': {'required':False},
            'time': {'required':False},
            'teacher': {'required':False},
        }