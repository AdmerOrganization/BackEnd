from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated 
from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.db import connection

from .serializers import Classroom_SearchSerializer
from .models import classroom
# Create your views here.

# Create Class API
class CreateClassAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    def post(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        classroom = serializer.save()
        user = request.user
        token = classroom.classroom_token

        subject = 'Class Token'
        html_message = render_to_string('1.html', {'nameholder': user.username , 'verifylink': absurl})
        plain_message = strip_tags(html_message)
        from_email = 'shanbeapp@gmail.com'
        to = user.email

        mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

        #return Response({
        #"user": UserSerializer(user, context=self.get_serializer_context()).data,
        #})



class Classroom_SearchAPI(generics.GenericAPIView):
    permission_classes = (IsAuthenticated,)

    queryset = ''
    serializer_class = Classroom_SearchSerializer
    def post(self, request, *args, **kwargs):

        serializer = self.get_serializer(data = request.data)
        serializer.is_valid(raise_exception=True)

        _title = serializer.data.get("title")
        _teacher_name = serializer.data.get("teacher_name")
        _time = serializer.data.get("time")
        _classes = classroom.objects.all()

        if _title:
            q = classroom.objects.filter(title=_title)
            _classes = (_classes&q)

        if _teacher_name:
            q = classroom.objects.filter(teacher_name=_teacher_name)
            _classes = (_classes&q)


        classes = set()
        if _time:
            for e in _classes:
                with connection.cursor() as cursor:
                    cursor.execute("SELECT id FROM `classrooms` WHERE TRIM(SUBSTRING_INDEX(time,'_',1)) LIKE %s", [_time[:10]])
                    templist = cursor.fetchall()

                class_ids = list(templist)

                temp_class = classroom.objects.filter(id__in = class_ids)
                if temp_class:
                    classes.add(e)

            serializer = (self.get_serializer(classes, many=True))

            return Response(serializer.data)
        
        serializer = (self.get_serializer(_classes, many=True))
        return Response(serializer.data)

# class DeleteSessionsAPI(generics.GenericAPIView):
#     serializer_class = Session_DeleteSerializer
#     permission_classes = (IsAuthenticated,)
#     def delete(self, request, *args, **kwargs):
#         serializer = self.get_serializer(data = request.data)

#         if serializer.is_valid():
#             if ('session_token' in serializer.data):
#                 sessionselect = session.objects.filter(session_token = serializer.data['session_token']).first()
#                 eventselect = sessionselect.event
#                 userselect = eventselect.userid
#                 if (userselect == request.user.id):

#                     try:
#                         users = sessionselect.users.all()
#                         email_plaintext_message = "Event title: {title} \nSession time: {time}".format(title=eventselect.title , time=sessionselect.time)
#                         for u in users:
                            
#                             send_mail(
#                                 # title:
#                                 "Session delete alert for {title}".format(title="Shanbe App"),
#                                 # message:
#                                 ".یکی از ملاقات هایی که شما داشتید توسط سازنده رویداد لغو شده است \n .لطفا برای ثبت تاریخ ملاقات جدید مجددا اقدام کنید \n" + ":مشخصات رویداد لغو شده به شرح زیر است\n" + email_plaintext_message,
#                                 # from:
#                                 "noreply@shanbe.local",
#                                 # to:
#                                 [u.email]
#                             )

#                         session.delete(sessionselect)
#                     except Exception as e:
#                         response = {
#                             'message': 'Session not found.',
#                         }
#                         return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
#                 else:
#                     response = {
#                             'message': 'User not allowed.',
#                         }
#                     return Response(response, status=status.HTTP_400_BAD_REQUEST)

#             else:
#                 response = {
#                     'message': 'session_token is required.',
#                 }
#                 return Response(response, status=status.HTTP_400_BAD_REQUEST)
                
#             response = {
#                 'status': 'success',
#                 'code': status.HTTP_200_OK,
#                 'message': 'Session deleted successfully',
#                 'data': []
#             }
#             return Response(response)

#         return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
