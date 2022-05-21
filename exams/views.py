from venv import create
from requests import options
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ExamInfoSerializer, ExamDataSerializer, ExamAnswerserializer
from .models import ExamInfo, ExamAnswers, ExamData
from rest_framework import status
import json


class ExamCreateAPI(generics.GenericAPIView):
    serializer_class = ExamInfoSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user.id
        exam_info = request.data.copy()
        # print(request.data)
        exam_info['creator'] = user

        serializer = self.get_serializer(data=exam_info)

        if serializer.is_valid(raise_exception=True):
            # pass
            serializer.save()
        
        new_exam_info = serializer.data['id']
        # print(new_exam_info, "*****")

        data = exam_info['data']
        # data = json.loads(data)
        # print(data[0])
        for exam_question in data:
            print(exam_question)
            options = exam_question[2:5]
            data_json = {
                'creator': user,
                'exam_info': new_exam_info,
                'question_num': exam_question[0],
                'question': exam_question[1],
                'options': str(options),
                'correct_answer': exam_question[6]
            }
            examdata_serializer = ExamDataSerializer(data=data_json)
            if examdata_serializer.is_valid(raise_exception=True):
                examdata_serializer.save()

        return Response(serializer.data)
    
    queryset = ""

    # def get(self, request, format=None):
    #     user = 74#request.user.id

    #     exam_Info = ExamInfo.objects.all()
    #     serializer = (self.get_serializer(exam_Info, many=True))

    #     exam_data = ExamData.objects.filter(creator=user)
    #     data_serializer = ExamDataSerializer(data=exam_data, many=True)
    #     if data_serializer.is_valid(raise_exception=True):
    #         print(data_serializer.data)

    #     for exam in serializer.data:
    #         print(exam['id'])

    #     return Response(serializer.data)



# class ExamInfoAPI(generics.GenericAPIView):
#     serializer_class = ExamInfoSerializer
#     # permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):
#         exam_info = request.data.copy()
#         print(request.data)
#         exam_info['creator'] = request.user.id

#         serializer = self.get_serializer(data=exam_info)

#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
        
#         return Response(serializer.data)
    
#     queryset = ""

#     def get(self, request, format=None):

#         exam_Info = ExamInfo.objects.all()
#         serializer = (self.get_serializer(exam_Info, many=True))

#         return Response(serializer.data)

# class ExamDataAPI(generics.GenericAPIView):
#     serializer_class = ExamDataSerializer
#     # permission_classes = (IsAuthenticated,)

#     def post(self, request, *args, **kwargs):

#         data_json = [{
#             'creator': request.user.id,
#             'exam_info': request.data['exam_info'],
#             'question': request.data['question'],
#             'options': json.dumps(request.data['answers']),
#         }]

#         serializer = self.get_serializer(data=data_json, many=True)

#         if serializer.is_valid(raise_exception=True):
#             serializer.save()
        
#         return Response(serializer.data)
    
#     queryset = ""
#     def get(self, request, format=None):

#         exam_data = ExamData.objects.all()
#         serializer = (self.get_serializer(exam_data, many=True))

#         return Response(serializer.data)


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