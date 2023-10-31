from django.db import models

#Model for Counter
class Counter(models.Model):
    flag = models.BooleanField()
    startTime = models.IntegerField()
    endTime = models.IntegerField()