from rest_framework import serializers
from .models import Counter

#Serializer for Events
class CounterSerializer(serializers.ModelSerializer):

    class Meta:
        model = Counter
        fields = ('flag', 'startTime', 'endTime')
    

