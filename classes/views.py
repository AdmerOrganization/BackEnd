
from logging import raiseExceptions
from rest_framework import generics
from rest_framework.response import Response
from .serializers import Classroom_CreateSerializer, Classroom_JoinSerializer, Classroom_SearchSerializer, Classroom_GetSerializer,\
    Classroom_DeleteSerializer, Classroom_EditSerializer, StudentSerializer
from .models import classroom, student
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from django.contrib.auth.hashers import make_password
from django.contrib.auth.hashers import check_password
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from .models import User
from homeworks.models import homework
from homeworks.serializers import Homework_DisplaySerializer
from exams.serializers import ExamInfoSerializer
from exams.models import ExamInfo
from datetime import datetime
# Create Class API

class CreateClassAPI(generics.GenericAPIView):
    serializer_class = Classroom_CreateSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        classroom = serializer.save(teacher=user)

        classroom.set_token()
        classroom.save()
        token = classroom.classroom_token

        subject = 'Class Token'

        html_message = render_to_string('4.html', {'classtoken': token})
        plain_message = strip_tags(html_message)
        from_email = 'shanbeapp@gmail.com'
        to = user.email

        mail.send_mail(subject, plain_message, from_email,
                       [to], html_message=html_message)

        return Response(Classroom_CreateSerializer(classroom, context=self.get_serializer_context()).data, status=status.HTTP_200_OK)


class JoinClassAPI(generics.GenericAPIView):
    serializer_class = Classroom_JoinSerializer
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        user = request.user
        selectclass = classroom.objects.filter(classroom_token = serializer.data['classroom_token']).first()
        if (selectclass == None):
            response = {
            'message': 'wrong class token.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        if (not check_password(serializer.data['password'], selectclass.password)):
            response = {
                'message': 'password is not correct.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        if (selectclass.teacher == request.user) :
            response = {
                'message': 'user is the teacher.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if selectclass.students.filter(id=request.user.id).exists():
            response = {
                'message': 'user already in classroom.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        
        if (selectclass.filled >= selectclass.limit):
            response = {
            'message': 'no space.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)
        selectclass.students.add(user)
        selectclass.filled = selectclass.filled + 1

        selectclass.save()

        response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'joined classroom successfully',
                'data': []
            }
        return Response(response)
       

class Classroom_SearchAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Classroom_SearchSerializer

    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        _title, _teacher_name, _time = "", "", ""

        if 'classroom_token' in request.data:
            _classroom_token = request.data["classroom_token"]
            _class = classroom.objects.filter(classroom_token=_classroom_token).first()
            if not _class:
                return Response("Wrong token")

            serializer = (self.get_serializer(_class))
            return Response(serializer.data)

        if 'title' in request.data:
            _title = request.data["title"]
        if 'teacher_name' in request.data:
            _teacher_name = request.data["teacher_name"]
        if 'time' in request.data:
            _time = request.data['time']

        _classes = classroom.objects.all()

        if _title:
            q = classroom.objects.filter(title=_title)
            _classes = (_classes & q)

        if _teacher_name:
            q = classroom.objects.filter(teacher_name=_teacher_name)
            _classes = (_classes & q)

        if _time:
            classes_times = classroom.objects.all().values('time', 'id')
            time_ids = []

            for i in range(len(classes_times)):
                if classes_times[i]['time'].strftime("%Y-%m-%d") == _time:
                    time_ids.append(classes_times[i]['id'])

            temp_class = classroom.objects.filter(id__in=time_ids)
            if temp_class:
                _classes = (_classes & temp_class)

            serializer = (self.get_serializer(_classes, many=True))

            return Response(serializer.data)

        serializer = (self.get_serializer(_classes, many=True))
        return Response(serializer.data)


class ListClasses(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Classroom_SearchSerializer
    queryset = ""

    def get(self, request, format=None):

        _classes = classroom.objects.all()
        serializer = (self.get_serializer(_classes, many=True))

        return Response(serializer.data)

class RetrieveClass(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Classroom_GetSerializer
    queryset = ""

    def post(self, request, format=None):
        class_id = request.data['id']

        _class = classroom.objects.filter(id=class_id).first()
        if not _class:
            return Response("Class doesnt exist", status.HTTP_400_BAD_REQUEST)
        
        serializer = (self.get_serializer(_class))
        return Response(serializer.data)


class ListCreatedClasses(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Classroom_GetSerializer
    queryset = ""

    def get(self, request, format=None):
        user_id = request.user.id

        _classes = classroom.objects.filter(teacher=user_id)
        serializer = (self.get_serializer(_classes, many=True))

        return Response(serializer.data)


class JoinedClasses(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = Classroom_GetSerializer
    queryset = ""

    def post(self, request, format=None):
        user = request.user

        class_ids = list(student.objects.filter(user_id=user.id).values_list('classroom_id', flat=True))

        classrooms = classroom.objects.filter(id__in = class_ids)

        serializer = (self.get_serializer(classrooms, many=True))

        return Response(serializer.data)


class ListClassesById(generics.ListAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = ""
    serializer_class = Classroom_GetSerializer
    def get(self, request, pk):
        classes = classroom.objects.filter(id=pk)
        serializer = Classroom_GetSerializer(classes, many=True)

        return Response(serializer.data)


class DeleteClassesAPI(generics.GenericAPIView):
    serializer_class = Classroom_DeleteSerializer
    permission_classes = (IsAuthenticated,)

    def delete(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)

        if serializer.is_valid():
            if ('classroom_token' in serializer.data):
                classselect = classroom.objects.filter(
                    classroom_token=serializer.data['classroom_token']).first()
                try:
                    classroom.delete(classselect)
                except Exception as e:
                    response = {
                        'message': 'Classroom not found.',
                    }
                    return Response(response, status=status.HTTP_400_BAD_REQUEST)
            else:
                response = {
                    'message': 'classroom_token is required.',
                }
                return Response(response, status=status.HTTP_400_BAD_REQUEST)

            response = {
                'status': 'success',
                'code': status.HTTP_200_OK,
                'message': 'Event deleted successfully',
                'data': []
            }
            return Response(response)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class EditClassAPI(generics.UpdateAPIView):
    serializer_class = Classroom_EditSerializer
    permission_classes = (IsAuthenticated,)

    def update(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        if ('classroom_token' in serializer.data):
            class_editing = classroom.objects.filter(
                classroom_token=serializer.data['classroom_token']).first()
        else:
            response = {
                'message': 'classroom_token is required.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if (class_editing == None):
            response = {
                'message': 'Classroom not found.',
            }
            return Response(response, status=status.HTTP_400_BAD_REQUEST)

        if(serializer.data.get("category") != None):
            class_editing.category = (serializer.data.get("category"))
        if(serializer.data.get("title") != None):
            class_editing.title = (serializer.data.get("title"))
        if(serializer.data.get("teacher_name") != None):
            class_editing.teacher_name = (serializer.data.get("teacher_name"))
        if(serializer.data.get("description") != None):
            class_editing.description = (serializer.data.get("description"))
        if(serializer.data.get("limit") != None):
            class_editing.limit = (serializer.data.get("limit"))
        if(serializer.data.get("password") != None):
            class_editing.password = make_password(
                serializer.data.get("password"))

        class_editing.save()

        response = {
            'status': 'success',
            'code': status.HTTP_200_OK,
            'message': 'Task updated successfully',
            'data': []
        }

        return Response(response)


class ClassStudentsAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    serializer_class = StudentSerializer
    queryset = ""

    def post(self, request, format=None):
        class_id = request.data['id']

        class_students = student.objects.filter(classroom_id=class_id).values('user_id')
        students_arr = []
        [students_arr.append(student['user_id']) for student in class_students]
        students = User.objects.filter(id__in = students_arr)
        serializer = self.get_serializer(students, many=True)


        return Response(serializer.data)


class LatestAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)
    queryset = ""

    def post(self, request, id):
        class_id = id
        time =  (datetime.now().astimezone().strftime('%Y-%m-%d'))
        selecthomework = homework.objects.filter(classroom_id = id , deadline__gte = time ).last()
        time =  (datetime.now().astimezone().strftime('%Y-%m-%d %H:%M:%S'))
        selectexam = ExamInfo.objects.filter(classroom_id = id , start_time__gte = time ).last()
        serializerH = Homework_DisplaySerializer(selecthomework).data
        serializerE = ExamInfoSerializer(selectexam).data
        responsedata = {}
        responsedata['homework'] = serializerH
        responsedata['exam'] = serializerE

        return Response(responsedata)