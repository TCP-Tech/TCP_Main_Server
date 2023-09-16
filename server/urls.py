from django.contrib import admin
from django.urls import path, include
from . import settings
from django.conf.urls.static import static


#url routing
urlpatterns = [
    path('server/admin/', admin.site.urls),
    path('', include('Events.urls')),
    path('', include('Speakers.urls')),
    path('', include('ProblemStatements.urls')),
    path('', include('Team.urls')),
]

urlpatterns += static(settings.MEDIA_URL, document_root = settings.MEDIA_ROOT)