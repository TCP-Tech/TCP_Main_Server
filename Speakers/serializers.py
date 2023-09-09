from rest_framework import serializers
from .models import Speaker

#Serializer for team data
class SpeakerSerializer(serializers.ModelSerializer):
    class Meta:
        model = Speaker
        fields = '__all__'