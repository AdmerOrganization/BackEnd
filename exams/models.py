from django.db import models
from accounts.models import User

# Create your models here.

class ExamInfo(models.Model):   #general exam data
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    questions_count = models.IntegerField()
    start_time = models.DateField()
    finish_time = models.DateField()

    class Meta:
        db_table = "exam_info"

class ExamData(models.Model):      #each question of said exam
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    exam_info = models.ForeignKey(to=ExamInfo, on_delete=models.CASCADE)
    question_num = models.IntegerField()
    question = models.CharField(max_length=64)
    options = models.CharField(max_length=128)
    correct_answer = models.CharField(max_length=128)

    class Meta:
        db_table = "exam_data"

class ExamAnswers(models.Model):       #user's answer to a single quesion of the exam
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    exam_data = models.ForeignKey(to=ExamData, on_delete=models.CASCADE)
    answers = models.CharField(max_length=64)

    class Meta:
        db_table = "exam_answers"
