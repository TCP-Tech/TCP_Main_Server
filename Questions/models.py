from django.db import models
from clients.models import Mentee
from django.utils import timezone
import datetime
from django.core.validators import MaxValueValidator, MinValueValidator

# Fix your choices format (tuples instead of sets)
DIFFICULTY_CHOICES = [
    ("1", "Easy"),
    ("2", "Medium"), 
    ("3", "Hard")
]

DSA_TOPIC_CHOICES = [
    ("1", "Array"),
    ("2", "Matrix"),
    ("3", "String"),
    ("4", "Search & Sort"),
    ("5", "Linked List"),
    ("6", "Binary Trees"),
    ("7", "BST"),
    ("8", "Greedy"),
    ("9", "Backtracking"),
    ("10", "Stacks & Queues"),
    ("11", "Heaps"),
    ("12", "Graphs"),
    ("13", "Tries"),
    ("14", "Dynamic Programming"),
    ("15", "Bit Manipulation")
]

SCOPE_CHOICES = [
    ("TEAM", "Team"),    # Default - only mentor's mentees
    ("ALL", "All")       # All mentees in system
]

class Question(models.Model):
    Qname = models.CharField(max_length=200, null=False)
    topic = models.CharField(max_length=200)
    Level = models.CharField(max_length=200, choices=DIFFICULTY_CHOICES)
    problemLink = models.URLField(max_length=200)
    description = models.CharField(max_length=300, blank=True, null=True)
    mentorId = models.IntegerField()
    scope = models.CharField(max_length=10, choices=SCOPE_CHOICES, default="TEAM")
    allotedTime = models.DateTimeField(default=timezone.now)
    SubmittedAt = models.DateTimeField(default=timezone.now, blank=True)
    submitedMentees = models.ManyToManyField(Mentee, blank=True)

    def __str__(self):
        return self.Qname

class QuestionAssignment(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    mentee = models.ForeignKey(Mentee, on_delete=models.CASCADE)
    assigned_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        unique_together = ('question', 'mentee')
