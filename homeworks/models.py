from django.db import models
from accounts.models import User
from classes.models import classroom, student
from uuid import uuid4
import os
from secrets import token_urlsafe
# Create your models here.


def path_and_rename(instance, filename):
    upload_to = 'files/homeworks'
    ext = filename.split('.')[-1]

    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

def path_and_rename_answer(instance, filename):
    upload_to = 'files/homeworks/asnwers'
    ext = filename.split('.')[-1]

    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)

class homework(models.Model):
    homework_token = models.CharField(max_length=500, blank=False, default='')
    file = models.FileField(
        upload_to=path_and_rename, blank=True, null=True)
    title = models.CharField(max_length=100, blank=False)
    description = models.TextField()
    deadline = models.CharField(max_length=100, blank=False)
    time = models.DateTimeField(auto_now_add=True)

    classroom = models.ForeignKey(
        classroom,
        on_delete=models.CASCADE,
    )

    def set_token(self, *args, **kwargs):
        if not self.homework_token:
            self.homework_token = token_urlsafe(16)

    class Meta:
        db_table = 'homeworks'


class answer (models.Model):
        file = models.FileField(
        upload_to=path_and_rename_answer, blank=False, null=False)

        homework = models.ForeignKey(homework, on_delete=models.CASCADE)
        user = models.ForeignKey(User, on_delete=models.CASCADE)

        