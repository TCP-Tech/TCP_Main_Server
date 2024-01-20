from rest_framework import serializers
from .models import *

class MentorSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mentor
        fields = '__all__'

class MenteeSerializer(serializers.ModelSerializer):
    
    class Meta:
        model = Mentee
        fields = '__all__'
#['name','email', 'username', 'password', 'branch', 'semester', 'phone_number', 'codechefID', 'codeforcesID', 'leetcodeID', 'gfgID', 'hackerrankID', 'linkedinID', 'score', 'total_q']

class MenteeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentee
        fields = ['image', 'name', 'phone_number','username', 'password', 'branch', 'semester', 'codechefID', 'codeforcesID', 'leetcodeID', 'gfgID', 'hackerrankID', 'linkedinID']
class MentorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['image', 'name', 'phone_number','username', 'password', 'branch', 'semester', 'codechefID', 'codeforcesID', 'leetcodeID', 'gfgID', 'hackerrankID', 'linkedinID']

class TeamSerializer(serializers.ModelSerializer):
   
    class Meta:
        model = Team
        fields = '__all__'
    team_members = MenteeSerializer(many=True, read_only=True)