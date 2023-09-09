from django.urls import path
from . import views

#url routing
urlpatterns = [
    path('server/problemstatements/<str:year>', views.problemStatementDataByYear),
    path('server/problemstatements/', views.problemStatementData),
]