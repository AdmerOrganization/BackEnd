from django.db import models
from django.conf import settings
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django_rest_passwordreset.signals import reset_password_token_created
from django.dispatch import receiver
from django.urls import reverse
from django_rest_passwordreset.signals import reset_password_token_created
from django.core.mail import send_mail  
from django.utils import timezone
import os
from uuid import uuid4

from django.core import mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags

# Create your models here.

@receiver(reset_password_token_created)
def password_reset_token_created(sender, instance, reset_password_token, *args, **kwargs):

    email_plaintext_message = format( reset_password_token.key)

    subject = 'Reset Password'
    html_message = render_to_string('2.html', {'changepasscode': email_plaintext_message})
    plain_message = strip_tags(html_message)
    from_email = 'shanbeapp@gmail.com'
    to = reset_password_token.user.email

    mail.send_mail(subject, plain_message, from_email, [to], html_message=html_message)

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