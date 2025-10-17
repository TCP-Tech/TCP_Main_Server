from django.db import models
from decouple import config

# Create your models here.

MEMBER_TYPE = (
        ('MNG', 'Manager'),
        ('HCO', 'Head Co-ordinator'),
        ('OCO', 'Overall Co-ordinator'),
        ('EXC', 'Executive'),
    )

Branches = [
    ['CSE']*2,
    ['IT']*2,
    ['ECE']*2,
    ['ELEC']*2,
    ['MECH']*2,
    ['CHEM']*2,
    ['CIVIL']*2,
    ['META']*2,
    ['MIN']*2,
    ['BIOMED']*2,
    ['BIOTECH']*2,
    ['MCA']*2
]

class TeamMember(models.Model):
    domain_choices = [
        ['Technical']*2,
        ['sponsorship']*2,
        ['PR & Marketing']*2,
        ['Documentation']*2,
        ['Design']*2,
        ['Video Editing']*2,
    ]

    name = models.CharField(max_length=100)
    branch = models.CharField(max_length=100, choices= Branches, default='CSE')
    image = models.ImageField(upload_to='static/uploads/team', null=True, blank = True)
    member_type = models.CharField(max_length=100, choices= MEMBER_TYPE, default='EXEC')
    year = models.IntegerField(default=2024)
    domain = models.CharField(max_length=100, choices=domain_choices, default='PR & Marketing')
    linkedin = models.URLField(blank=True, null=True)
    instagram = models.URLField(blank=True, null=True)
    email = models.EmailField(blank=True, null=True)
    drive_image_url= models.URLField(blank=True, null= True)


    # @property
    # def image_url(self):
    #     return config('HOST')+self.image.url


    def __str__(self):
        return f'{self.member_type} - {self.name} --({self.year})'
