# Generated by Django 3.2.8 on 2022-04-24 21:02

from django.db import migrations, models
import django.db.models.deletion
import homeworks.models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('classes', '0005_auto_20220425_0128'),
    ]

    operations = [
        migrations.CreateModel(
            name='homework',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('homework_token', models.CharField(default='', max_length=500)),
                ('file', models.FileField(blank=True, null=True, upload_to=homeworks.models.path_and_rename)),
                ('title', models.CharField(max_length=100)),
                ('description', models.TextField()),
                ('deadline', models.CharField(max_length=100)),
                ('time', models.DateTimeField(auto_now_add=True)),
                ('answers', models.ManyToManyField(related_name='answers_homeworks', to='classes.student')),
                ('classroom', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='classes.classroom')),
            ],
            options={
                'db_table': 'homeworks',
            },
        ),
    ]