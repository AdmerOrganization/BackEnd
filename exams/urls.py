from django.urls import path, include
from .views import ExamCreateAPI, ExamInfoRetrieveAPI, ExamAnswersAPI, ExamDataRetrieveAPI, ExamStartAnsweringAPI,\
     ExamFinishAnsweringAPI, ExamCalculateResultAPI, ExamEditAPI, StudentsResultsExamAPI

urlpatterns = [
    path('exams_create/', ExamCreateAPI.as_view(), name='ExamCreateAPI'),
    path('exams_edit/', ExamEditAPI.as_view(), name='ExamEditAPI'),
    path('exams_retrieve/', ExamInfoRetrieveAPI.as_view(), name='ExamRetrieveAPI'),
    path('data_retrieve/', ExamDataRetrieveAPI.as_view(), name='ExamDataRetrieveAPI'),
    path('start_answer/', ExamStartAnsweringAPI.as_view(), name='ExamStartAnsweringAPI'),
    path('finish_answer/', ExamFinishAnsweringAPI.as_view(), name='ExamFinishAnsweringAPI'),
    path('answer/', ExamAnswersAPI.as_view(), name='ExamAnswersAPI'),
    path('calculate/', ExamCalculateResultAPI.as_view(), name='ExamCalculateResultAPI'),
    path('students_results/', StudentsResultsExamAPI.as_view(), name='StudentsResultsExamAPI'),
]
