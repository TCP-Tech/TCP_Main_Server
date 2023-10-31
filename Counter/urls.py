from django.urls import path, include
from . import views

#url routing
urlpatterns = [
    path('server/setcounter/', views.startTimer),
    path('server/getcounter/', views.getStartTime),
]