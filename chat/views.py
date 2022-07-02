from re import S
import re
import unicodedata
from django.shortcuts import render
from chat.serializers import Classroom_TokenSerializer
from rest_framework import generics, permissions, status
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from knox.models import AuthToken
from classes.models import classroom
# Create your views here.
"""
class chatAPI(generics.GenericAPIView):


    
    def post(self, request):
        return render(request, 'chat/index.html', {
        'room_name': 'room_test'
    })
"""

class ChatAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    def get(self, request, id):
        
        user = request.user
        token = AuthToken.objects.filter(user=user).first()

        try:
            selectclass = classroom.objects.get(id = id)
        except:
            return Response({'error': 'Classroom doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)
        return render(request, 'chat/room.html', {
            'room_name': selectclass.classroom_token,
            'token': token.token_key,
            'classroom': selectclass.classroom_token
        })


class GetClassTokenAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Classroom_TokenSerializer
    def get(self, request, id):

        try:
            selectclass = classroom.objects.get(id = id)
        except:
            return Response({'error': 'Classroom doesnt exist'}, status=status.HTTP_400_BAD_REQUEST)

        serializer = (self.get_serializer(selectclass))
        return Response(serializer.data)