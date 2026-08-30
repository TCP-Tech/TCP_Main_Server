from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('server/team/<int:year>/', views.get_members),
    path('server/team/member/', views.create_or_update_member),
    # path('team_years/', views.team_years)   to get the years for which teams data is stored.
]