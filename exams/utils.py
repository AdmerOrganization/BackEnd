from .models import ExamAnswers, ExamGrades, ExamData, ExamInfo
from .serializers import ExamGradesSerializer, ExamDataSerializer

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
    user_answers = ExamAnswers.objects.get(user=userid, exam_info=examid).answers
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
