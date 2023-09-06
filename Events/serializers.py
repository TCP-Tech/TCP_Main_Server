from rest_framework import serializers
from .models import Event

#Serializer for Events
class EventSerializer(serializers.ModelSerializer):
    class Meta:
        model = Event
        fields = ['year','title','date','img','description','instaLink']