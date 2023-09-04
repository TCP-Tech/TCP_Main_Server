from django.contrib import admin
from django.urls import path
from . import views

#url routing
urlpatterns = [
    path('server/admin/', admin.site.urls),
    path('server/team/', views.teamData),
    path('server/team/<str:year>', views.teamDataByYear),
]
