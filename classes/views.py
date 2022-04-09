from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from classes.serializers import Classroom_CreateSerializer
from .models import classroom
from accounts.models import User
from rest_framework import generics, status
from django.conf import settings
from rest_framework.authtoken.serializers import AuthTokenSerializer
from knox.views import LoginView as KnoxLoginView
from django.contrib.auth import login
from rest_framework.fields import CharField, EmailField, ImageField
from rest_framework.permissions import IsAuthenticated 
from datetime import datetime

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

from django.template import loader
from django.http import HttpResponse

# Create your views here.

# Create Class API
class CreateClassAPI(generics.GenericAPIView):
    serializer_class = Classroom_CreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        classroom = serializer.save(teacher = user)
        
        classroom.set_token()
        classroom.save()
        token = classroom.classroom_token

        subject = 'Class Token'
        
        html_message = render_to_string('2.html', {'changepasscode': token})
        plain_message = strip_tags(html_message)
        from_email = 'shanbeapp@gmail.com'
        to = user.email

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Response({
        "classroom": Classroom_CreateSerializer(classroom, context=self.get_serializer_context()).data,
        }, status=status.HTTP_200_OK)
