from django.db.models.base import Model
from rest_framework import fields, serializers
from django.contrib.auth.models import User
from rest_framework import viewsets
from rest_framework.fields import CharField
from .models import classroom


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