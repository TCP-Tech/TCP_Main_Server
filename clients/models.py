from django.db import models
from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import AbstractUser
from django.core.serializers import serialize
# Create your models here.
# Mentor model

Branches = (
    ("1" , "CSE"),
    ("2" , "IT"),
    ("3" , "ECE"),
    ("4" , "ELEC"),
    ("5" , "MECH"),
    ("6" , "CHEM"),
    ("7" , "CIVIL"),
    ("8" , "META"),
    ("9" , "MIN"),
    ("10" , "BIOMED"),
    ("11" , "BIOTECH"),
    ("12" , "MCA"),
)

class Mentor(models.Model):
    name = models.CharField(max_length=200, null=False)
    username = models.CharField(max_length=200,null=False,unique=True)
    password = models.CharField(max_length=200)
    branch = models.CharField(max_length=10,choices=Branches)
    semester = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(8)])
    phone_number = models.CharField(max_length=10,unique=True)
    codechefID = models.URLField(max_length=100,null=True)
    codeforcesID = models.URLField(max_length=100,null=True)
    leetcodeID = models.URLField(max_length=100,null=True)
    gfgID = models.URLField(max_length=100,null=True)
    hackerrankID = models.URLField(max_length=100,null=True)
    linkedinID = models.URLField(max_length=100)
    score = models.BigIntegerField(default=0)
    total_q = models.BigIntegerField(default=0)
    
    def allotted_teams(self):
        teams=  Team.objects.filter(alloted_mentor=self)
        return teams
    
    def __str__(self):
        return self.username
class Mentee(models.Model):
    name = models.CharField(max_length=200, null=False)
    username = models.CharField(max_length=200,null=False,unique=True)
    password = models.CharField(max_length=200)
    branch = models.CharField(max_length=10,choices=Branches)
    semester = models.IntegerField(validators=[MinValueValidator(1),MaxValueValidator(8)])
    phone_number = models.CharField(max_length=10,unique=True)
    codechefID = models.URLField(max_length=100)
    codeforcesID = models.URLField(max_length=100)
    leetcodeID = models.URLField(max_length=100)
    gfgID = models.URLField(max_length=100)
    hackerrankID = models.URLField(max_length=100, null=True)
    linkedinID = models.URLField(max_length=100)
    score = models.BigIntegerField(default=0)
    total_q = models.BigIntegerField(default=0)
    mentor_id = models.IntegerField(default = 0, null=True)
    
    def get_team(self):
        teams =  Team.objects.filter(team_members=self)
        return teams
    
    def __str__(self):
        return self.username




class Team(models.Model):
    team_name       = models.CharField(max_length=50,null=False)
    alloted_mentor = models.ForeignKey(Mentor, on_delete=models.SET_NULL, null=True, blank=True)
    team_members = models.ManyToManyField(Mentee)
    team_score      = models.IntegerField(default=0)
    
    
    def __str__(self):
        return self.team_name    
    

    
