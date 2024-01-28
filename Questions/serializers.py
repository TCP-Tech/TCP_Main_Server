from rest_framework import serializers
from .models import *
from clients.serializers import MenteeQuestion


class QuestionSerializer(serializers.ModelSerializer):

    submitedMentees=MenteeQuestion(many=True)
    class Meta:
        model = Question
        fields = '__all__'
       
    formated_allotedtime = serializers.DateTimeField(source='allotedTime', format='%d-%m-%Y %H:%M:%S %Z%z ', read_only=True)

class addQuestionSerializer(serializers.ModelSerializer):

    # submitedMentees=MenteeQuestion(many=True)
    class Meta:
        model = Question
        fields = '__all__'
       
    formated_allotedtime = serializers.DateTimeField(source='allotedTime', format='%d-%m-%Y %H:%M:%S %Z%z ', read_only=True)