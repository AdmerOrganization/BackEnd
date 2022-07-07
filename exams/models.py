from django.db import models
from accounts.models import User
from classes.models import classroom

# Create your models here.

class ExamInfo(models.Model):   #general exam data
    creator = models.ForeignKey(to=User, on_delete=models.CASCADE)
    classroom =  models.ForeignKey(to=classroom, on_delete=models.CASCADE)
    name = models.CharField(max_length=64)
    questions_count = models.IntegerField()
    start_time = models.DateTimeField(auto_now=True)
    finish_time = models.DateTimeField(auto_now=True)

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
    exam_info = models.ForeignKey(to=ExamInfo, on_delete=models.CASCADE)
    answers = models.CharField(max_length=128)

    class Meta:
        db_table = "exam_answers"

class ExamGrades(models.Model):
    user = models.ForeignKey(to=User, on_delete=models.CASCADE)
    exam_info = models.ForeignKey(to=ExamInfo, on_delete=models.CASCADE)
    grade = models.CharField(max_length=64, blank=True)
    visible = models.BooleanField(default=False)
    finished = models.BooleanField(default=False)
    started = models.BooleanField(default=False)
    
    class Meta:
        db_table = "exam_grades"
