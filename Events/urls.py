from django.urls import path, include
from . import views

#url routing
urlpatterns = [
    path('server/events/<str:year>', views.eventDataByYear),
    path('server/events/', views.eventData),
]