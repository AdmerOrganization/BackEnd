# Generated by Django 3.2.8 on 2022-04-26 11:41

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('exams', '0004_examdata_creator'),
    ]

    operations = [
        migrations.RenameField(
            model_name='examdata',
            old_name='answers',
            new_name='options',
        ),
    ]
