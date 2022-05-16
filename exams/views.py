from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ExamInfoSerializer, ExamDataSerializer, ExamAnswerserializer
from .models import ExamInfo, ExamAnswers, ExamData
from rest_framework import status
import json

class ExamInfoAPI(generics.GenericAPIView):
    serializer_class = ExamInfoSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        exam_info = request.data.copy()
        print(request.data)
        exam_info['creator'] = request.user.id

        serializer = self.get_serializer(data=exam_info)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data)
    
    queryset = ""

    def get(self, request, format=None):

        exam_Info = ExamInfo.objects.all()
        serializer = (self.get_serializer(exam_Info, many=True))

        return Response(serializer.data)

class ExamDataAPI(generics.GenericAPIView):
    serializer_class = ExamDataSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        data_json = [{
            'creator': request.user.id,
            'exam_info': request.data['exam_info'],
            'question': request.data['question'],
            'options': json.dumps(request.data['answers']),
        }]

        serializer = self.get_serializer(data=data_json, many=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data)
    
    queryset = ""
    def get(self, request, format=None):

        exam_data = ExamData.objects.all()
        serializer = (self.get_serializer(exam_data, many=True))

        return Response(serializer.data)


class ExamAnswersAPI(generics.GenericAPIView):
    serializer_class = ExamAnswerserializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):

        data_json = [{
            'user': 72,#request.user.id,
            'exam_data': request.data['exam_data'],
            'answers': json.dumps(request.data['answers']),
        }]

        serializer = self.get_serializer(data=data_json, many=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data)