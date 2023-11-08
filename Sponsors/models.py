from django.db import models
from decouple import config

#Model for Sponsors
class Sponsor(models.Model):
    
    year = models.CharField(max_length=5)
    type = models.CharField(max_length=25)
    img = models.ImageField(upload_to="static/uploads/Sponsors/", null = True, blank=True)
    