# Generated by Django 3.2.8 on 2022-05-20 15:32

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='ExamInfo',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=64)),
                ('questions_count', models.IntegerField()),
                ('start_time', models.DateField()),
                ('finish_time', models.DateField()),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exam_info',
            },
        ),
        migrations.CreateModel(
            name='ExamData',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('question_num', models.IntegerField()),
                ('question', models.CharField(max_length=64)),
                ('options', models.CharField(max_length=128)),
                ('correct_answer', models.CharField(max_length=128)),
                ('creator', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
                ('exam_info', models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='exams.examinfo')),
            ],
            options={
                'db_table': 'exam_data',
            },
        ),
        migrations.CreateModel(
            name='ExamAnswers',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('answers', models.CharField(max_length=64)),
                ('exam_data', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='exams.examdata')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'db_table': 'exam_answers',
            },
        ),
    ]
