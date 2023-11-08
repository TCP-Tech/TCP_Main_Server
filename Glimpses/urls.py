from django.urls import path, include
from . import views

#url routing
urlpatterns = [
    path('server/glimpses/<str:year>', views.GlimpseDataByYear),
    path('server/glimpses/', views.GlimpseData),
]