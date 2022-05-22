from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ExamInfoSerializer, ExamDataSerializer, ExamAnswerSerializer, ExamGradesSerializer
from .models import ExamInfo, ExamAnswers, ExamData, ExamGrades
from rest_framework import status
import json
from .utils import has_panel, is_finished, is_started, answer_to_data_exists

class ExamCreateAPI(generics.GenericAPIView):
    serializer_class = ExamInfoSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = 74#request.user.id
        exam_info = request.data.copy()
        # print(request.data)
        exam_info['creator'] = user

        serializer = self.get_serializer(data=exam_info)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        new_exam_info = serializer.data['id']

        data = exam_info['data']
        for exam_question in data:
            print(exam_question)
            options = exam_question[2:6]
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


    def orderdict_to_list(self,order_dict):
        list = []
        for i in order_dict:
           list.append(dict(i))
        return list


    queryset = ""

    def get(self, request, format=None):
        user = 65#request.user.id

        exam_Info = ExamInfo.objects.filter(creator=user)
        serializer = (self.get_serializer(exam_Info, many=True))
        ExamInfo_list = self.orderdict_to_list(serializer.data)

        exam_data = ExamData.objects.filter(creator=user)
        data_serializer = ExamDataSerializer(exam_data, many=True)
        ExamData_list = self.orderdict_to_list(data_serializer.data)

        result = []

        for exam_info in ExamInfo_list:
            data = {
                "id": exam_info["id"],
                "name": exam_info['name'],
                "questions_count": exam_info['questions_count'],
                "start_time": exam_info['start_time'],
                "finish_time": exam_info['finish_time'],
                "data": []
            }
            for exam_data in ExamData_list:
                examdata = {
                    'question_num': exam_data['question_num'],
                    'question': exam_data['question'],
                    'options': exam_data['options'],
                    'correct_answer': exam_data['correct_answer'],
                }
                if exam_data['exam_info'] == exam_info['id']:
                    data['data'].append(examdata)
            
            result.append(data)


        return Response(result, status=status.HTTP_200_OK)

class ExamInfoRetrieveAPI(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = ExamInfoSerializer
    queryset = ""
    
    def orderdict_to_list(self,order_dict):
        list = []
        for i in order_dict:
           list.append(dict(i))
        return list
    

    def post(self, request, format=None):
        id = request.data['id']
        user = 74#request.user.id

        exam_Info = ExamInfo.objects.filter(creator=user)
        serializer = (self.get_serializer(exam_Info, many=True))
        ExamInfo_list = self.orderdict_to_list(serializer.data)

        exam_data = ExamData.objects.filter(creator=user)
        data_serializer = ExamDataSerializer(exam_data, many=True)
        ExamData_list = self.orderdict_to_list(data_serializer.data)

        result = []

        for exam_info in ExamInfo_list:
            data = {
                "id": exam_info["id"],
                "name": exam_info['name'],
                "questions_count": exam_info['questions_count'],
                "start_time": exam_info['start_time'],
                "finish_time": exam_info['finish_time'],
                "data": []
            }
            for exam_data in ExamData_list:
                examdata = {
                    'question_num': exam_data['question_num'],
                    'question': exam_data['question'],
                    'options': exam_data['options'],
                    'correct_answer': exam_data['correct_answer'],
                }
                if exam_data['exam_info'] == exam_info['id']:
                    data['data'].append(examdata)
            
            result.append(data)

        answer = {}
        for i in result:
            if i['id'] == id:
                answer = i

        return Response(answer, status=status.HTTP_200_OK)

class ExamDataRetrieveAPI(generics.GenericAPIView):
    # permission_classes = (IsAuthenticated,)
    serializer_class = ExamDataSerializer
    queryset = ""
    
    def post(self, request, format=None):
        id = request.data['exam_info']
        user = 74#request.user.id
        question_num = request.data['question_num']
        data_obj = ExamData.objects.filter(creator = user, exam_info=id, question_num=question_num).first()
        serializer = self.get_serializer(data_obj)
        if 'id' not in serializer.data.keys():
            return Response("Question doesn't exist")
        return Response(serializer.data['id'], status=status.HTTP_200_OK)

class ExamAnswersAPI(generics.GenericAPIView):
    serializer_class = ExamAnswerSerializer
    # permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = 74#request.user.id

        data_json = [{
            'user': user,
            'exam_data': request.data['exam_data'],
            'answers': json.dumps(request.data['answers']),
        }]

        exam_info = ExamData.objects.filter(id=request.data['exam_data']).values('exam_info')[0]['exam_info']

        if not is_started(user, exam_info) or not has_panel(user, exam_info):
            return Response("You have to start the exam first")

        if is_finished(user, exam_info):
            return Response("User has already finished this exam")

        if answer_to_data_exists(user, request.data['exam_data']):
            return Response("User has already answered this question")

        serializer = self.get_serializer(data=data_json, many=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExamStartAnsweringAPI(generics.GenericAPIView):
    serializer_class = ExamGradesSerializer

    def post(self, request, *args, **kwargs):
        id = request.data['exam_info']
        user = 74#request.user.id
        request.data['user'] = user
        request.data['started'] = True

        if not has_panel(user, id):
            serializer = self.get_serializer(data=request.data)
            if serializer.is_valid(raise_exception=True):
                serializer.save()
        
            return Response(serializer.data)
        else:
            if is_started(user, id):
                return Response("Exam already started")
            else:
                ExamGrades.objects.filter(user = user, exam_info = id).update(started=True)
                return Response("Panel already existed so just started the exam for the student")

class ExamFinishAnsweringAPI(generics.GenericAPIView):
    serializer_class = ExamGradesSerializer

    def post(self, request, *args, **kwargs):
        id = request.data['exam_info']
        user = 74#request.user.id
        request.data['user'] = user
        request.data['started'] = True

        if not is_started(user, id) or not has_panel(user, id):
            return Response("You have to start the exam first")
        
        if is_finished(user, id):
            return Response("User has already finished this exam")

        ExamGrades.objects.filter(user = user, exam_info = id).update(finished=True)
        return Response("Successfully Finished the exam!")

class ExamCalculateResultAPI(generics.GenericAPIView):
    serializer_class = ExamGradesSerializer

    def post(self, request, *args, **kwargs):
        id = request.data['exam_info']
        user = 74#request.user.id
        request.data['user'] = user
        request.data['started'] = True

        if is_started(user, id) and has_panel(user, id) and is_finished(user, id):
            exam_grade = ExamGrades.objects.filter(user = user, exam_info = id).first()
            serializer = ExamGradesSerializer(exam_grade)
            return Response(serializer.data)
        return Response("Error calculating result")
