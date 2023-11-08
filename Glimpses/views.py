from django.shortcuts import render
from .models import Glimpse
from .serializers import GlimpseSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


#view to get Glimpses by year
@api_view(['GET'])
def GlimpseDataByYear(request, year):
    Glimpses = Glimpse.objects.all().filter(year = year)
    res_data = GlimpseSerializer(Glimpses, many = True, context={'request': request}).data
 
    if len(Glimpses):
        res_message = "Glimpses Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Glimpses Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)

#view to get Glimpses 
@api_view(['GET'])
def GlimpseData(request):
    Glimpses = Glimpse.objects.all()
    res_data = GlimpseSerializer(Glimpses, many = True, context={'request': request}).data

    if len(Glimpses):
        res_message = "Glimpses Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Glimpses Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)
 