from django.urls import path
from . import views
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView,TokenBlacklistView


urlpatterns = [
    path('mentor/token/', TokenObtainPairView.as_view(), name='mentor_token_obtain_pair'),
    path('mentor/token/refresh/', TokenRefreshView.as_view(), name='mentor_token_refresh'),
    path('server/mentor_login', views.mentorLogin),
    path('server/mentee_login', views.menteeLogin),
    path('server/mentee_signup', views.menteeRegister),
    path('server/get-team-mentor/<id>', views.get_team_mentor),
    path('server/get-team-mentee/<id>', views.get_team_mentee),
    path('server/update_mentee', views.updateMenteeProfile),
    path('server/update_mentor', views.updateMentorProfile),
    path('server/getTeams/', views.Getteams),
    path('server/getMentees/', views.Getmentees),
    path('server/getMentee/<menteeId>', views.GetmenteeDetail),
    path('server/getMentor/<mentorId>', views.GetmentorDetail),
    path('server/createteam', views.createTeam),
    path('server/updateteam', views.updateTeam),
    path('server/mentor/logout/', views.mentor_logout, name='mentor_logout'),
    path('server/mentee/logout/', views.mentee_logout, name='mentee_logout'),
]
