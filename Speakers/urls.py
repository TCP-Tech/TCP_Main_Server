from django.urls import path, include
from . import views

#url routing
urlpatterns = [
    path('server/speakers/<str:year>', views.speakerDataByYear),
    path('server/speakers/', views.speakerData),
]