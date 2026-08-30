from rest_framework import serializers
from .models import *

class TeamDetailSerializer(serializers.ModelSerializer):
    class Meta:
        model = Team
        fields = '__all__'

class MentorSerializer(serializers.ModelSerializer):
    Mentorteam = TeamDetailSerializer(read_only=True)
    class Meta:
        model = Mentor
        fields = '__all__'

class MenteeSerializer(serializers.ModelSerializer):
    Menteeteam = TeamDetailSerializer(read_only=True)
    class Meta:
        model = Mentee
        fields = '__all__'
    
#['name','email', 'username', 'password', 'branch', 'semester', 'phone_number', 'codechefID', 'codeforcesID', 'leetcodeID', 'gfgID', 'hackerrankID', 'linkedinID', 'score', 'total_q']
class MentorGetSerializer(serializers.ModelSerializer):
    Mentorteam = TeamDetailSerializer(read_only=True)
    class Meta:
        model = Mentor
        exclude = ['email', 'password','phone_number']

class MenteeGetSerializer(serializers.ModelSerializer):
    Menteeteam = TeamDetailSerializer(read_only=True)
    class Meta:
        model = Mentee
        exclude = ['email', 'password','phone_number']
    
class MenteeUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentee
        fields = ['image','mentor_id', 'name', 'phone_number','username', 'password', 'branch', 'semester', 'codechefID', 'codeforcesID', 'leetcodeID', 'gfgID', 'hackerrankID', 'linkedinID']

class MentorUpdateSerializer(serializers.ModelSerializer):
    class Meta:
        model = Mentor
        fields = ['image', 'name', 'phone_number', 'password', 'branch', 'semester', 'codechefID', 'codeforcesID', 'leetcodeID', 'gfgID', 'hackerrankID', 'linkedinID']

class TeamSerializer(serializers.ModelSerializer):
    team_members = MenteeGetSerializer(many=True, read_only=True)
    alloted_mentor = MentorGetSerializer(read_only=True)
    class Meta:
        model = Team
        fields = '__all__'

#data of mentees to be displayed after submission of question
class MenteeQuestion(serializers.ModelSerializer):
   
    class Meta:
        model = Mentee
        fields = ['id','name']