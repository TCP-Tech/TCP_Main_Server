from django.urls import path, include
from . import views

#url routing
urlpatterns = [
    path('server/sponsors/<str:year>', views.sponsorDataByYear),
    path('server/sponsors/', views.sponsorData),
]