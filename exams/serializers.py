from rest_framework import serializers
from .models import ExamAnswers, ExamData, ExamInfo, ExamGrades


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

class ExamAnswerSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamAnswers
        fields = "__all__"
        extra_kwargs={
            'user': {'required': False},
        }

class ExamGradesSerializer(serializers.ModelSerializer):

    class Meta:
        model = ExamGrades
        fields = "__all__"
        extra_kwargs={
            'user': {'required': False},
        }