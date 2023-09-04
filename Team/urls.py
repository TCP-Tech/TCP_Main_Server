from django.contrib import admin
from django.urls import path
from . import views

#url routing
urlpatterns = [
    path('admin/', admin.site.urls),
    path('team/', views.teamData),
    path('team/<str:year>', views.teamDataByYear),
]
