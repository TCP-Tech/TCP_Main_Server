from django.urls import path, include
from . import views

#url routing
urlpatterns = [
    path('server/winners/<str:year>', views.WinnerDataByYear),
    path('server/winners/', views.WinnerData),
]