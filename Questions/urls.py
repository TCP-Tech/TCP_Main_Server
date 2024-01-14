from django.urls import path
from . import views

urlpatterns = [
    path('server/addQuestion', views.QuestionRegister),
    path('server/getQuestions', views.GetQuestion),
    path('server/submitQuestion', views.Onsubmit)
]