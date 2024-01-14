from rest_framework import serializers
from .models import *


class QuestionSerializer(serializers.ModelSerializer):

    
    class Meta:
        model = Question
        fields = '__all__'
    formated_allotedtime = serializers.DateTimeField(source='allotedTime', format='%d-%m-%Y %H:%M:%S %Z%z ', read_only=True)