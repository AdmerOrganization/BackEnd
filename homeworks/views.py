from logging import raiseExceptions
from select import select
from turtle import home
from rest_framework import generics
from rest_framework.response import Response

from classes.models import classroom, student
from .serializers import Homework_AnswerSerializer, Homework_CreateSerializer, Homework_DisplaySerializer, Homework_EditSerializer, Homework_ListSerializer
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

class DisplayHomeworkAPI(generics.GenericAPIView):
    serializer_class = Homework_DisplaySerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        token = serializer.validated_data['homework_token']
        selecthomework = homework.objects.get(homework_token = token)
        selectclass = selecthomework.classroom

        students = student.objects.filter(classroom_id = selectclass.id)
        if (selecthomework == None):
            return Response({'error': 'Homework doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        if(user not in students and user != selectclass.teacher): # should check for TA ...
            return Response({'error': 'User is not a student or the teacher'}, status=status.HTTP_403_FORBIDDEN)


        return Response(Homework_DisplaySerializer(selecthomework, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)

class ListHomeworkAPI(generics.GenericAPIView):
    serializer_class = Homework_ListSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        selectclass = serializer.validated_data['classroom']

        if (selectclass == None):
            return Response({'error': 'Classroom doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        students = student.objects.filter(classroom_id = selectclass.id)

        if(user not in students and user != selectclass.teacher): # should check for TA ...
            return Response({'error': 'User is not a student or the teacher'}, status=status.HTTP_403_FORBIDDEN)

        homeworks = homework.objects.filter (classroom_id = selectclass.id)
        serializer = (self.get_serializer(homeworks, many=True))
        return Response(serializer.data)
        

class AnswerHomeworkAPI(generics.GenericAPIView):
    serializer_class = Homework_AnswerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user

        token = serializer.validated_data['homework_token']
        selecthomework = homework.objects.get(homework_token = token)
        selectclass = selecthomework.classroom

        students = student.objects.filter(classroom_id = selectclass.id)
        if (selecthomework == None):
            return Response({'error': 'Homework doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        if(user not in students and user != selectclass.teacher): # should check for TA ...
            return Response({'error': 'User is not a student or the teacher'}, status=status.HTTP_403_FORBIDDEN)


        return Response(Homework_DisplaySerializer(selecthomework, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)
