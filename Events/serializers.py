from rest_framework import serializers
from .models import Event

#Serializer for Events
class EventSerializer(serializers.ModelSerializer):

    class Meta:
        model = Event
        fields = '__all__'
    

