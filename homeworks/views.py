from logging import raiseExceptions
from turtle import home
from rest_framework import generics
from rest_framework.response import Response

from classes.models import classroom
from .serializers import Homework_CreateSerializer
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
        print (serializer.validated_data)
        selectclass = serializer.validated_data['classroom']

        if (selectclass == None):
            return Response({'error': 'Classroom doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        if(user != selectclass.teacher):
            return Response({'error': 'User is not the teacher'}, status=status.HTTP_403_FORBIDDEN)

        homework = serializer.save(classroom=selectclass)

        homework.set_token()
        homework.save()

        return Response(Homework_CreateSerializer(homework, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)

