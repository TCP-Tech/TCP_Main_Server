from django.shortcuts import render
from .models import Event
from .serializers import EventSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


#view to get events by year
@api_view(['GET'])
def eventDataByYear(request, year):
    events = Event.objects.all().filter(year = year)
    res_data = EventSerializer(events, many = True, context={'request': request}).data
 
    if len(events):
        res_message = "Events Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Events Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)

#view to get events 
@api_view(['GET'])
def eventData(request):
    events = Event.objects.all()
    res_data = EventSerializer(events, many = True, context={'request': request}).data

    if len(events):
        res_message = "Events Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Events Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)
 