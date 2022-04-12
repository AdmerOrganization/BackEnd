from rest_framework import generics, permissions
from rest_framework.response import Response
from knox.models import AuthToken

from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.db import connection
from rest_framework_simplejwt.tokens import RefreshToken
import jwt

from .serializers import Classroom_CreateSerializer, Classroom_SearchSerializer
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
        
        html_message = render_to_string('4.html', {'classtoken': token})
        plain_message = strip_tags(html_message)
        from_email = 'shanbeapp@gmail.com'
        to = user.email

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        return Response({
        "classroom": Classroom_CreateSerializer(classroom, context=self.get_serializer_context()).data,
        }, status=status.HTTP_200_OK)



class Classroom_SearchAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = ''
    serializer_class = Classroom_SearchSerializer
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        _title = serializer.data.get("title")
        _teacher_name = serializer.data.get("teacher_name")
        _time = serializer.data.get("time")
        _classes = classroom.objects.all()

        if _title:
            q = classroom.objects.filter(title=_title)
            _classes = (_classes&q)

        if _teacher_name:
            q = classroom.objects.filter(teacher_name=_teacher_name)
            _classes = (_classes&q)


        classes = set()
        if _time:
            for e in _classes:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM `classrooms` WHERE TRIM(SUBSTRING_INDEX(time,'_',1)) LIKE %s", [_time[:10]])
                    templist = cursor.fetchall()

                class_ids = list(templist)

                temp_class = classroom.objects.filter(id__in = class_ids)
                if temp_class:
                    classes.add(e)

            serializer = (self.get_serializer(classes, many=True))

            return Response(serializer.data)
        
        serializer = (self.get_serializer(_classes, many=True))
        return Response(serializer.data)