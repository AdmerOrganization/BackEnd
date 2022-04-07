from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from rest_framework_simplejwt.tokens import RefreshToken
import jwt
from .models import User, UserProfile
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
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        classroom = serializer.save()
        user = request.user
        token = classroom.classroom_token

        subject = 'Class Token'
        html_message = render_to_string('1.html', {'nameholder': user.username , 'verifylink': absurl})
        plain_message = strip_tags(html_message)
        from_email = 'shanbeapp@gmail.com'
        to = user.email

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        #return Response({
        #"user": UserSerializer(user, context=self.get_serializer_context()).data,
        #})
