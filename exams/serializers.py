from rest_framework import serializers
from .models import ExamAnswers, ExamData, ExamInfo


class ExamInfoSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamInfo
        fields = "__all__"
        extra_kwargs={
            'creator': {'required': False},
        }

class ExamDataSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamData
        fields = "__all__"
        extra_kwargs={
            'creator': {'required': False},
        }

class ExamAnswerserializer(serializers.ModelSerializer):

    class Meta:
        model = ExamAnswers
        fields = "__all__"
        extra_kwargs={
            'user': {'required': False},
        }