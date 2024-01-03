from django.urls import path
from . import views

urlpatterns = [
    path('server/login', views.mentorLogin),
]
