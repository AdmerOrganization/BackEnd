from rest_framework import serializers
from django.contrib.auth.models import User
from .models import classroom
from django.contrib.auth.hashers import make_password
import django.contrib.auth.password_validation as validators


class Classroom_CreateSerializer(serializers.ModelSerializer):
    class Meta:
        model = classroom
        fields = ('id', 'password', 'classroom_token', 'title', 'avatar',
                  'teacher_name', 'description', 'limit', 'teacher_id' ,'category')
        extra_kwargs = {
            'classroom_token': {'read_only': True, 'required': False},
            'id': {'read_only': True, 'required': False},
            'password': {'required': True, 'write_only': True},
        }

    def validate_password(self, data):
        validators.validate_password(password=data, user=User)
        return data

    def create(self, validated_data):
        validated_data['password'] = make_password(
            validated_data.get('password'))
        return super(Classroom_CreateSerializer, self).create(validated_data)


class Classroom_JoinSerializer(serializers.ModelSerializer):
    class Meta:
        model = classroom
        fields = ('password', 'classroom_token')
        extra_kwargs = {
            'classroom_token': {'required': True},
            'password': {'required': True},
        }


class Classroom_SearchSerializer(serializers.ModelSerializer):
    is_joined = serializers.SerializerMethodField()
    class Meta:
        model = classroom
        fields = ('id', 'classroom_token', 'title', 'teacher_name', 'time','is_joined')
        extra_kwargs = {
            'classroom_token': {'read_only': True, 'required': False},
            'id': {'read_only': True, 'required': False},
            'title': {'required': False},
            'teacher_name': {'required': False},
            'time': {'required': False},
        }
    def get_is_joined(self, obj):
        request = self.context.get('request', None)
        user = request.user
        if (user in obj.students.all()):
            return 1
        else :
            return 0


class Classroom_GetSerializer(serializers.ModelSerializer):
    class Meta:
        model = classroom
        fields = ('id', 'classroom_token', 'avatar', 'title',
                  'teacher_name', 'description', 'limit', 'time', 'category')
        extra_kwargs = {
            'classroom_token': {'read_only': True, 'required': True},
        }



class Classroom_DeleteSerializer(serializers.ModelSerializer):
    class Meta:
        model = classroom
        fields = ('id', 'classroom_token')


class Classroom_EditSerializer(serializers.ModelSerializer):
    class Meta:
        model = classroom
        fields = ('id', 'classroom_token', 'avatar', 'title',
                  'teacher_name', 'description', 'limit', 'time', 'category')
        extra_kwargs = {
            'title': {'required': False},
            'teacher_name': {'required': False},
            'time': {'required': False},
            'limit': {'required': False},
            'description': {'required': False},
            'password': {'required': False},
            'teacher': {'required': False},
        }