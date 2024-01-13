from rest_framework import serializers
from .models import *

class MentorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mentee
        fields = ['name', 'username', 'password', 'branch', 'semester', 'phone_number', 'codechefID', 'codeforcesID', 'leetcodeID', 'gfgID', 'hackerrankID', 'linkedinID', 'score', 'total_q']

class MenteeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mentee
        fields = '__all__'
#['name', 'username', 'password', 'branch', 'semester', 'phone_number', 'codechefID', 'codeforcesID', 'leetcodeID', 'gfgID', 'hackerrankID', 'linkedinID', 'score', 'total_q']
class TeamSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'