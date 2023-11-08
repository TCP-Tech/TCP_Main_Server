from rest_framework import serializers
from .models import ShortlistedTeam

#Serializer for ShortlistedTeams
class ShortlistedTeamSerializer(serializers.ModelSerializer):

    class Meta:
        model = ShortlistedTeam
        fields = '__all__'
    

