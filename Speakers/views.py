from django.shortcuts import render
from .models import Speaker
from .serializers import SpeakerSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


#view to get speakers by year
@api_view(['GET'])
def speakerDataByYear(request, year):
    speakers = Speaker.objects.all().filter(year = year)
    res_data = SpeakerSerializer(speakers, many = True, context={'request': request}).data

    if len(speakers):
        res_message = "Speakers Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Speakers Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)

#view to get speakers 
@api_view(['GET'])
def speakerData(request):
    speakers = Speaker.objects.all()
    res_data = SpeakerSerializer(speakers, many = True, context={'request': request}).data

    if len(speakers):
        res_message = "Speakers Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Speakers Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)
 