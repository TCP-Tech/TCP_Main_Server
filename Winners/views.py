from django.shortcuts import render
from .models import Winner
from .serializers import WinnerSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


#view to get Winners by year
@api_view(['GET'])
def WinnerDataByYear(request, year):
    Winners = Winner.objects.all().filter(year = year)
    res_data = WinnerSerializer(Winners, many = True, context={'request': request}).data
 
    if len(Winners):
        res_message = "Winners Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Winners Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)

#view to get Winners 
@api_view(['GET'])
def WinnerData(request):
    Winners = Winner.objects.all()
    res_data = WinnerSerializer(Winners, many = True, context={'request': request}).data

    if len(Winners):
        res_message = "Winners Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Winners Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)
 