from rest_framework import serializers
from .models import TeamData

#Serializer for team data
class TeamDataSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamData
        fields = ['year', 'data']
