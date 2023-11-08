from django.db import models
from decouple import config

#Model for problem statements
class ProblemStatement(models.Model):
    
    year = models.CharField(max_length=5)
    title = models.CharField(max_length=50)
    domain = models.CharField(max_length=50)  
    background = models.TextField(max_length=2000, blank=True)
    statement = models.TextField(max_length=2000, blank=True)
    impact = models.TextField(max_length=2000, blank=True)
    img = models.ImageField(upload_to="problemStatements/", null = True, blank=True)
    

    @property
    def image_url(self):
        return config('HOST')+self.img.url    
