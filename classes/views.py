import imp
from django.shortcuts import render
from rest_framework import generics, status
from serializers import Classroom_SearchSerializer
from django.db import connection
# Create your views here.


class Classroom_SearchAPI(generics.GenericAPIView):
    serializer_class = Classroom_SearchSerializer
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        
        return Response(serializer.data)