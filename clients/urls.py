from django.urls import path
from . import views

urlpatterns = [
    path('server/mentor_login', views.mentorLogin),
    path('server/mentee_login', views.menteeLogin),
    path('server/mentee_signup', views.menteeRegister),
    path('server/get-team-mentor/<id>', views.get_team_mentor),
    path('server/get-team-mentee/<id>', views.get_team_mentee),
    path('server/update_mentee', views.updateMenteeProfile),
    path('server/update_mentor', views.updateMentorProfile),
    path('server/getTeams', views.Getteams)
]
