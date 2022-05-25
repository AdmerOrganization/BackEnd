from rest_framework import serializers
from django.contrib.auth.models import User

from classes.models import classroom
from classes.serializers import Classroom_GetSerializer
from .models import Message
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators


class MessageSerializer(serializers.ModelSerializer):
    sender = serializers.SlugRelatedField(many=False, slug_field='username', queryset=User.objects.all())

    class Meta:
        model = Message
        fields = ['sender', 'receiver', 'message', 'timestamp']
