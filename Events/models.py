from django.db import models

#Model for events
class Event(models.Model):
    year = models.CharField(max_length=5)
    title = models.CharField(max_length=100)
    date = models.CharField(max_length=25)
    img = models.ImageField(upload_to="media/")
    description = models.TextField(max_length=2000, blank=True)
    instaLink = models.CharField(max_length=100, blank=True)