# Generated by Django 3.2.8 on 2022-05-22 11:21

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0005_alter_examgrades_exam_info'),
    ]

    operations = [
        migrations.AlterField(
            model_name='examgrades',
            name='exam_info',
            field=models.OneToOneField(on_delete=django.db.models.deletion.CASCADE, to='exams.examinfo'),
        ),
    ]
