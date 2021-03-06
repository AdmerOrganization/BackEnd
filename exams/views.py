from unittest import result
from rest_framework.permissions import IsAuthenticated
from rest_framework import generics
from rest_framework.response import Response
from .serializers import ExamInfoSerializer, ExamDataSerializer, ExamAnswerSerializer, ExamGradesSerializer
from .models import ExamInfo, ExamAnswers, ExamData, ExamGrades
from rest_framework import status
import json
from .utils import has_panel, is_finished, is_started, answer_to_exam_exists, calcuate_exam_answer,\
     merge_two_dicts, user_exam_score, handle_ending_exam_after_legaltime, update_exam_result
from classes.models import classroom as Classroom
from accounts.models import User

class ExamCreateAPI(generics.GenericAPIView):
    serializer_class = ExamInfoSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user.id
        exam_info = request.data.copy()
        exam_info['creator'] = user

        serializer = self.get_serializer(data=exam_info)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        new_exam_info = serializer.data['id']
        data = exam_info['data']
        for exam_question in data:
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
        user = request.user.id

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
                "classroom": exam_info['classroom'],
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

class ExamEditAPI(generics.UpdateAPIView):
    serializer_class = ExamInfoSerializer
    permission_classes = (IsAuthenticated,)
    
    def orderdict_to_list(self,order_dict):
        list = []
        for i in order_dict:
           list.append(dict(i))
        return list

    def update(self, request, *args, **kwargs):
        user = request.user.id
        id = request.data['id']
        examinfo_obj = ExamInfo.objects.filter(id=id).first()
        serializer = ExamInfoSerializer(examinfo_obj, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        if "data" in request.data.keys():
            if request.data['data']:
                exam_data = ExamData.objects.filter(creator=user, exam_info=id)
                data_serializer = ExamDataSerializer(exam_data, many=True)
                ExamData_list = self.orderdict_to_list(data_serializer.data)
                for data in ExamData_list:
                    ExamData.objects.get(id=data["id"]).delete()
                
                for exam_question in request.data['data']:
                    options = exam_question[2:6]
                    data_json = {
                        'creator': user,
                        'exam_info': id,
                        'question_num': exam_question[0],
                        'question': exam_question[1],
                        'options': str(options),
                        'correct_answer': exam_question[6]
                    }
                    examdata_serializer = ExamDataSerializer(data=data_json)
                    if examdata_serializer.is_valid(raise_exception=True):
                        examdata_serializer.save()

        return Response(serializer.data, status=status.HTTP_200_OK)

class ExamInfoRetrieveAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExamInfoSerializer
    queryset = ""
    
    def orderdict_to_list(self,order_dict):
        list = []
        for i in order_dict:
           list.append(dict(i))
        return list
    

    def post(self, request, format=None):
        user_id = request.user.id

        exam_Info = ExamInfo.objects.all()
        serializer = (self.get_serializer(exam_Info, many=True))
        ExamInfo_list = self.orderdict_to_list(serializer.data)

        exam_data = ExamData.objects.all()
        data_serializer = ExamDataSerializer(exam_data, many=True)
        ExamData_list = self.orderdict_to_list(data_serializer.data)

        result = []

        for exam_info in ExamInfo_list:
            handle_ending_exam_after_legaltime(user_id, exam_info["id"])
            data = {
                "id": exam_info["id"],
                "name": exam_info['name'],
                "classroom": exam_info['classroom'],
                "questions_count": exam_info['questions_count'],
                "start_time": exam_info['start_time'],
                "finish_time": exam_info['finish_time'],
                "score": user_exam_score(user_id, exam_info["id"]),
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

        answer = []

        for i in result:
            if "id" in request.data.keys():
                if i['id'] == request.data['id']:
                    answer.append(i)
            elif "classroom" in request.data.keys():
                if "title" in request.data.keys() and i['classroom'] == request.data['classroom']:
                    if request.data['title'] in i["name"]:
                        answer.append(i)
                elif i['classroom'] == request.data['classroom']:
                    answer.append(i)
                

        return Response(answer, status=status.HTTP_200_OK)

class ExamDataRetrieveAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = ExamDataSerializer
    queryset = ""
    
    def post(self, request, format=None):
        id = request.data['exam_info']
        user = request.user.id
        data_obj = ExamData.objects.filter(creator = user, exam_info=id)
        serializer = self.get_serializer(data_obj, many=True)
        result = []
        for i in serializer.data:
            result.append(i)

        return Response(result , status=status.HTTP_200_OK)

class ExamAnswersAPI(generics.GenericAPIView):
    serializer_class = ExamAnswerSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        user = request.user.id

        data_json = [{
            'user': user,
            'exam_info': request.data['exam_info'],
            'answers': json.dumps(request.data['answers']),
        }]

        #exam_info = ExamData.objects.filter(id=request.data['exam_data']).values('exam_info')[0]['exam_info']
        exam_info = request.data['exam_info']

        if not is_started(user, exam_info) or not has_panel(user, exam_info):
            return Response("You have to start the exam first")

        if is_finished(user, exam_info):
            return Response("User has already finished this exam")

        if answer_to_exam_exists(user, request.data['exam_info']):
            return Response("User has already answered this exam")

        if  len(request.data['answers']) != ExamInfo.objects.get(id=exam_info).questions_count:
            return Response("Number of answers you\'ve returned is not equal to this exams questions count")

        serializer = self.get_serializer(data=data_json, many=True)

        if serializer.is_valid(raise_exception=True):
            serializer.save()
        
        return Response(serializer.data, status=status.HTTP_200_OK)

class ExamStartAnsweringAPI(generics.GenericAPIView):
    serializer_class = ExamGradesSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        id = request.data['exam_info']
        user = request.user.id
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
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        id = request.data['exam_info']
        user = request.user.id
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
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        id = request.data['exam_info']
        user = request.user.id
        request.data['user'] = user

        if not is_finished(user, id) or not has_panel(user, id):
            return Response("You have to finish the exam first", status=status.HTTP_404_NOT_FOUND)

        if has_panel(user, id) and is_finished(user, id):
            update_exam_result(user, id)
            exam_grade = ExamGrades.objects.filter(user = user, exam_info = id).first()
            serializer = ExamGradesSerializer(exam_grade)
            return Response(serializer.data['grade'], status=status.HTTP_200_OK)

        return Response("Error calculating result")

class StudentsResultsExamAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        teacher_id = request.user.id
        exam_id = request.data['exam_info']
        classroom_id = request.data['classroom_id']

        examinfo_obj = ExamInfo.objects.filter(id=exam_id).first()
        classroom_obj =  Classroom.objects.filter(id=classroom_id).first()
        if classroom_obj.teacher_id != teacher_id:
            return Response("This user is not this classroom's teacher!")
        if teacher_id != examinfo_obj.creator_id:
            return Response("This teacher is not the creator of this test!")
        
        class_users_queryset = Classroom.objects.filter(id=classroom_obj.id).values('students')
        class_users_list = []
        for i in class_users_queryset:
            class_users_list.append(int(i['students']))

        examgrades_obj = ExamGrades.objects.filter(exam_info=examinfo_obj.id, user__in=class_users_list)
        
        class_users_done_exam = []
        for examgrade_obj in examgrades_obj:
            class_users_done_exam.append(examgrade_obj.user_id)
        
        result = []

        for student_id in class_users_list:
            temp = {
                "first_name": User.objects.get(id=student_id).first_name,
                "last_name": User.objects.get(id=student_id).last_name
            }
            if student_id in class_users_done_exam:
                handle_ending_exam_after_legaltime(student_id, exam_id)
                temp = merge_two_dicts(temp, {
                    "score": examgrades_obj[class_users_done_exam.index(student_id)].grade
                })
            else:
                temp = merge_two_dicts(temp, {
                    "score": "N/A"
                })

            result.append(temp)
        
        return Response(result)
        
