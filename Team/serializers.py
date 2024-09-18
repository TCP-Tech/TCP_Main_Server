from rest_framework import serializers
from .models import TeamMembers


class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = TeamMembers
        fields = '__all__'
    