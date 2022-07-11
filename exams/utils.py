from datetime import datetime
import pytz
from .models import ExamAnswers, ExamGrades, ExamData, ExamInfo
from .serializers import ExamGradesSerializer, ExamDataSerializer
from .models import ExamInfo, ExamAnswers, ExamData, ExamGrades

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

def answer_to_exam_exists(userid,examid):
    temp = ExamAnswers.objects.filter(user = userid, exam_info = examid)
    if temp:
        return True
    return False

def calcuate_exam_answer(userid, examid):
    user_answers_obj = ExamAnswers.objects.filter(user=userid, exam_info=examid).first()
    if not user_answers_obj:
        return "0.0"
    user_answers = user_answers_obj.answers
    data_obj = ExamData.objects.filter(exam_info=examid)
    examdata_serializer = ExamDataSerializer(data_obj, many=True)
    result = []
    for i in examdata_serializer.data:
        result.append(i)
    correct_answers = []
    for i in result:
        correct_answers.append(i['correct_answer'])
    
    user_answers = user_answers[1:-1].split(',')

    exam_questions_count = ExamInfo.objects.get(id=examid).questions_count
    num_correct_answers = 0
    for i in range(len(correct_answers)):
        if int(correct_answers[i]) == int(user_answers[i]):
            num_correct_answers += 1
    return(round(num_correct_answers/exam_questions_count, 2) * 100)

def merge_two_dicts(x, y):
    z = x.copy()
    z.update(y) 
    return z

def user_exam_score(user_id, exam_info_id):
    obj = ExamGrades.objects.filter(user = user_id, exam_info_id=exam_info_id).first()
    exam_info_obj = ExamInfo.objects.get(id=exam_info_id)
    if obj:
        if obj.finished is True and datetime.now() < exam_info_obj.finish_time:
            return "Exam has not ended yet"
        return obj.grade
    return "N/A"

def handle_ending_exam_after_legaltime(user_id, exam_info_id):
    exam_grade = ExamGrades.objects.filter(user = user_id, exam_info = exam_info_id).first()
    exam_info_obj = ExamInfo.objects.get(id=exam_info_id)
    if datetime.now() > exam_info_obj.finish_time and exam_grade:
        update_exam_result(user_id, exam_info_id)

def update_exam_result(user_id, exam_info_id):
    exam_grade = ExamGrades.objects.filter(user = user_id, exam_info = exam_info_id).first()
    if not ExamGrades.objects.filter(id=exam_grade.id).first().grade:
        result_percentage = calcuate_exam_answer(user_id, exam_info_id)
        ExamGrades.objects.filter(id=exam_grade.id).update(grade=str(result_percentage))