from rest_framework import serializers
from .models import Winner

#Serializer for Winners
class WinnerSerializer(serializers.ModelSerializer):

    class Meta:
        model = Winner
        fields = '__all__'
    
