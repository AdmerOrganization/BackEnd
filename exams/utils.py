from .models import ExamAnswers, ExamGrades
from .serializers import ExamGradesSerializer

def has_panel(userid, examinfoid):
    temp = ExamGrades.objects.filter(user = userid, exam_info = examinfoid)
    if temp:
        return True
    return False

def is_started(userid, examinfoid):
    temp = ExamGrades.objects.filter(user = userid, exam_info = examinfoid).first()
    serializer = ExamGradesSerializer(temp)
    started = serializer.data['started']
    if started:
        return True
    return False

def is_finished(userid, examinfoid):
    temp = ExamGrades.objects.filter(user = userid, exam_info = examinfoid).first()
    serializer = ExamGradesSerializer(temp)
    finished = serializer.data['finished']
    if finished:
        return True
    return False

def answer_to_data_exists(userid,dataid):
    temp = ExamAnswers.objects.filter(user = userid, exam_data = dataid)
    if temp:
        return True
    return False