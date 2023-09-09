from django.db import models
from decouple import config

#Model for speakers
class Speaker(models.Model):
    
    year = models.CharField(max_length=5)
    name = models.CharField(max_length=50)
    position = models.CharField(max_length=50)
    img = models.ImageField(upload_to="media/", null = True, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    facebook = models.CharField(max_length=100, blank=True)
    twitter = models.CharField(max_length=100, blank=True)
    linkedIn = models.CharField(max_length=100, blank=True)
    github = models.CharField(max_length=100, blank=True)
    youtube = models.CharField(max_length=100, blank=True)
    

    @property
    def image_url(self):
        return config('HOST')+self.img.url    