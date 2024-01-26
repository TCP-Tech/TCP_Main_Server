from django.db import models
from clients.models import Mentee
from django.utils.timezone import utc
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

difficulty={
    ("1","Easy"),
    ("2","Medium"),
    ("3","Hard")
}

DSA_topic={
    ("1","Array"),
    ("2","Matrix"),
    ("3","String"),
    ("4","Search & Sort"),
    ("5","Linked List"),
    ("6","Binary Trees"),
    ("7","BST"),
    ("8","Greedy"),
    ("9","Backtracking"),
    ("10","Stacks & Queues"),
    ("11","Heap"),
    ("12","Graph"),
    ("13","Trie"),
    ("14","Dynammic Programming"),
    ("15","Bit Manupilation")
}

class Question(models.Model):
    Qname = models.CharField(max_length=200, null=False)
    topic = models.CharField(max_length=200)
    Level = models.CharField(max_length=200)
    problemLink =models.URLField(max_length=200)
    description= models.CharField(max_length=300,blank=True,null=True)
    mentorId = models.IntegerField()
    allotedTime= models.DateTimeField(default=timezone.now)
    SubmittedAt = models.DateTimeField(default=timezone.now,blank=True)
    submitedMentees=models.ManyToManyField(Mentee)
   

    def add_value(self, new_value):
        # Add a new value to the comma-separated values
        if self.submittedmenteeId:
            self.submittedmenteeId += f",{new_value}"
        else:
            self.submittedmenteeId = new_value
        self.save()

    def get_values_as_list(self):
        # Return the comma-separated values as a list
        return self.submittedmenteeId.split(',')


   

    def __str__(self):
        return self.Qname
    
    
    
   

    

    
    
   
