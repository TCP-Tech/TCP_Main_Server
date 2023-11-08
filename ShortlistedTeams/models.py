from django.db import models
from decouple import config

#Model for ShortlistedTeams
class ShortlistedTeam(models.Model):
    
    year = models.CharField(max_length = 5)
    name = models.CharField(max_length = 100)
    openInnovation = models.BooleanField(default = False)
    member1 = models.CharField(max_length = 100, null = True)
    member2 = models.CharField(max_length = 100, null = True)
    member3 = models.CharField(max_length = 100, null = True)
    member4 = models.CharField(max_length = 100, null = True)
    member5 = models.CharField(max_length = 100, null = True)
    member6 = models.CharField(max_length = 100, null = True)
