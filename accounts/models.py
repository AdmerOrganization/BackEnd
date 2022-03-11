from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save


from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  

from django.utils import timezone
import os
from uuid import uuid4
# Create your models here.


# Change filename to user_id
def path_and_rename(instance, filename):
    upload_to = 'images/userProfile'
    ext = filename.split('.')[-1]

    filename = '{}.{}'.format(uuid4().hex, ext)
    # return the whole path to the file
    return os.path.join(upload_to, filename)


class UserProfile(models.Model):
    avatar = models.ImageField(upload_to=path_and_rename, blank=True ,null=True)
    phone_number = models.CharField(max_length=13, null=True, blank=True)
    is_verified = models.BooleanField(default=False)
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        primary_key=True,
    )