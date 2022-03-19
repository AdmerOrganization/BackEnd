from rest_framework import serializers
from django.contrib.auth.models import User
from django.forms import ValidationError
from rest_framework.fields import CharField, EmailField, ImageField
import re

# User Serializer
class UserSerializer(serializers.ModelSerializer):
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name')

# User Serializer
class CurrentUserSerializer(serializers.ModelSerializer):
    phone_number = serializers.SerializerMethodField()
    avatar = serializers.SerializerMethodField()

    def get_phone_number(self, obj):
        return obj.userprofile.phone_number

    def get_avatar(self, obj):
        try:
            return (obj.userprofile.avatar.url)
        except Exception as e:
            return "None"

    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'first_name', 'last_name', 'phone_number', 'avatar')


# Verify Email Token Serializer
class EmailVerificationSerializer(serializers.ModelSerializer):
    token = serializers.CharField(max_length=555)
    class Meta:
        model = User

        fields = ['token']

# Signup Serializer
class SignUpSerializer(serializers.ModelSerializer):
    password2 = CharField(label='Confirm Password')
    class Meta:
        model = User
        fields = ('id', 'username', 'email', 'password', 'password2','first_name', 'last_name')
        extra_kwargs = {
            'password': {'write_only': True},
            'password2': {'write_only': True},
            "email": {'required': True }
        }

    def validate_email(self, value):
        norm_email = value.lower()
        if User.objects.filter(email=norm_email).exists():
            raise serializers.ValidationError("Your email is already registered!")
        return norm_email

    def validate(self, data):
        password = data.get('password')
        confirm_password = data.pop('password2')
        if password != confirm_password:
            raise ValidationError('Passwords dont match!')
        elif len(password) < 8:
            raise ValidationError("Make sure your password is at lest 8 letters")
        elif re.search('[0-9]',password) is None:
            raise ValidationError("Make sure your password has a number in it")
        elif re.search('[A-Z]',password) is None: 
            raise ValidationError("Make sure your password has a capital letter in it")
        return data

    def create (self, validated_data):
        email = validated_data.get('email')
        username = validated_data.get('username')
        password = validated_data.get('password')
        
        try:
            user = User.objects.create(username=username, email=email)
            user.set_password(password)
            user.first_name = validated_data['first_name']
            user.last_name  = validated_data['last_name']
            user.save()
            return user
        except Exception as e:
            return e


# Edit Profile Serializer
class EditSerializer(serializers.ModelSerializer):

    email = EmailField(required = False)
    avatar = ImageField(use_url=True, required=False)
    first_name = CharField(max_length=32, required=False)
    last_name = CharField(max_length=32, required=False)
    phone_number = CharField(max_length=13,min_length=8, required=False)

    class Meta:
        model = User
        fields = ('id', 'email', 'first_name' , 'last_name' , 'avatar' , 'phone_number')
        extra_kwargs = {
            'first_name': {'required': False},
            'last_name': {'required': False},
            "email": {'required': False },
            "phone_number": {'required': False },
            "avatar": {'required': False}
        }


    def validate_email(self, value):
        user = self.context['request'].user
        print(user)
        norm_email = value.lower()
        if (norm_email == user.email):
            return norm_email
        if User.objects.filter(email=norm_email):
            raise serializers.ValidationError("Your email is already registered!")
        return norm_email


