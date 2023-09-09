from rest_framework import serializers
from .models import ProblemStatement

#Serializer for problem statements
class ProblemStatementSerializer(serializers.ModelSerializer):

    class Meta:
        model = ProblemStatement
        fields = '__all__'
    
