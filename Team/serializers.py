from rest_framework import serializers
from .models import TeamMember


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMember
        fields = '__all__'
    