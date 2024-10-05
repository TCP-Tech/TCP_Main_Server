from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('server/team/<int:year>/', views.get_members),
    # path('team_years/', views.team_years)   to get the years for which teams data is stored.
]