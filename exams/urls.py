from django.urls import path, include
from knox import views as knox_views
from django.conf import settings
from django.conf.urls.static import static
from .views import ExamInfoAPI, ExamDataAPI, ExamAnswersAPI

urlpatterns = [
    path('exams_info/', ExamInfoAPI.as_view(), name='ExamInfoAPI'),
    path('exams_data/', ExamDataAPI.as_view(), name='ExamDataAPI'),
    path('exams_answers/', ExamAnswersAPI.as_view(), name='ExamAnswersAPI'),
]
