# Generated by Django 3.2.8 on 2022-04-15 17:05

from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('classes', '0003_alter_classroom_teacher'),
    ]

    operations = [
        migrations.AddField(
            model_name='classroom',
            name='category',
            field=models.TextField(default='none'),
        ),
        migrations.AddField(
            model_name='classroom',
            name='filled',
            field=models.IntegerField(default=0),
        ),
        migrations.AddField(
            model_name='classroom',
            name='users',
            field=models.ManyToManyField(related_name='user_class', to=settings.AUTH_USER_MODEL),
        ),
    ]