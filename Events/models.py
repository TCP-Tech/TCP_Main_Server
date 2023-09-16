from django.db import models
from decouple import config

#Model for events
class Event(models.Model):
    
    year = models.CharField(max_length=5)
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=25)
    img = models.ImageField(upload_to="static/uploads/events/", null = True, blank=True)
    description = models.TextField(max_length=2000, blank=True)
    instaLink = models.CharField(max_length=100, blank=True)

    # @property
    # def image_url(self):
    #     return config('HOST')+self.img.url    
