from django.shortcuts import render
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response


#view to get events by year
@api_view(['GET'])
def eventDataByYear(request, year):
    eventsData = Event.objects.all().filter(year = year)
    rtr = EventSerializer(eventsData, many = True)
    return Response(rtr.data)

#view to get events 
@api_view(['GET'])
def eventData(request):
    eventsData = Event.objects.all()
    rtr = EventSerializer(eventsData, many = True)
    return Response(rtr.data)
 