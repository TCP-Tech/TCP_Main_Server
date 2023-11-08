from django.urls import path, include
from . import views

#url routing
urlpatterns = [
    path('server/shotlistedTeams/<str:year>', views.ShortlistedTeamData),
    path('server/shotlistedTeams/', views.ShortlistedTeamDataByYear),
]