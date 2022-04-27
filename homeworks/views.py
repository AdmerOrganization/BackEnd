from logging import raiseExceptions
from select import select
from turtle import home
from rest_framework import generics
from rest_framework.response import Response

from classes.models import classroom
from .serializers import Homework_CreateSerializer, Homework_EditSerializer
from .models import homework
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your views here.


class CreateHomeworkAPI(generics.GenericAPIView):
    serializer_class = Homework_CreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        selectclass = serializer.validated_data['classroom']

        if (selectclass == None):
            return Response({'error': 'Classroom doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        if(user != selectclass.teacher): # should check for TA ...
            return Response({'error': 'User is not the teacher'}, status=status.HTTP_403_FORBIDDEN)

        

        homework = serializer.save(classroom=selectclass)

        homework.set_token()
        homework.save()

        return Response(Homework_CreateSerializer(homework, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)


class EditHomeworkAPI(generics.GenericAPIView):
    serializer_class = Homework_EditSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        token = serializer.validated_data['homework_token']
        selecthomework = homework.objects.get(homework_token = token)


        if (selecthomework == None):
            return Response({'error': 'Homework doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        selectclass = selecthomework.classroom

        if (selectclass == None):
            return Response({'error': 'Classroom doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        if(user != selectclass.teacher): # should check for TA ...
            return Response({'error': 'User is not the teacher'}, status=status.HTTP_403_FORBIDDEN)

        if(serializer.data.get("file") != None):
            selecthomework.file = (serializer.data.get("file"))
        if(serializer.data.get("title") != None):
            selecthomework.title = (serializer.data.get("title"))
        if(serializer.data.get("description") != None):
            selecthomework.description = (serializer.data.get("description"))
        if(serializer.data.get("deadline") != None):
            selecthomework.deadline = (serializer.data.get("deadline"))

        selecthomework.save()

        return Response(Homework_EditSerializer(selecthomework, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)

