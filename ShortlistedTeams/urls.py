from django.urls import path, include
from . import views

#url routing
urlpatterns = [
    path('server/shortlistedTeams/<str:year>', views.ShortlistedTeamDataByYear),
    path('server/shortlistedTeams/', views.ShortlistedTeamData),
]