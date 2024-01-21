from django.urls import path
from . import views

urlpatterns = [
    path('server/addQuestion', views.QuestionRegister),
    path('server/getQuestions/<mentorId>', views.GetQuestion),
    path('server/submitQuestion', views.Onsubmit)
]