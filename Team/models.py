from django.db import models
from django.db.models import JSONField

#Model for teams section
class TeamData(models.Model):
    year = models.CharField(max_length=5)
    data = JSONField()
