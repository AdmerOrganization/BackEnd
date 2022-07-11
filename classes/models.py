from django.db import models
from accounts.models import User
from uuid import uuid4
import os
from secrets import token_urlsafe
# Create your models here.


def path_and_rename(instance, filename):
    upload_to = 'images/classroom'
    ext = filename.split('.')[-1]

    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class classroom(models.Model):
    classroom_token = models.CharField(max_length=500, blank=False, default='')
    avatar = models.ImageField(
        upload_to=path_and_rename, blank=True, null=True)
    category = models.TextField(default='none')
    title = models.CharField(max_length=100, blank=False)
    teacher_name = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    limit = models.IntegerField(blank=False)
    filled = models.IntegerField(blank=False, default=0)
    time = models.DateTimeField(auto_now_add=True)
    password = models.CharField(max_length=500)

    students = models.ManyToManyField(User, through='student')

    teacher = models.ForeignKey(
        User,
        on_delete=models.CASCADE,
        related_name='teacher'
    )

    def set_token(self, *args, **kwargs):
        if not self.classroom_token:
            self.classroom_token = token_urlsafe(16)

    class Meta:
        db_table = 'classrooms'

class student(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    classroom = models.ForeignKey(classroom, on_delete=models.CASCADE)
    date_joined = models.DateTimeField(auto_now_add=True)