from django.shortcuts import render
from .models import Sponsor
from .serializers import SponsorSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


#view to get Sponsors by year
@api_view(['GET'])
def sponsorDataByYear(request, year):
    Sponsors = Sponsor.objects.all().filter(year = year)
    res_data = SponsorSerializer(Sponsors, many = True, context={'request': request}).data
 
    if len(Sponsors):
        res_message = "Sponsors Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Sponsors Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)

#view to get Sponsors 
@api_view(['GET'])
def sponsorData(request):
    Sponsors = Sponsor.objects.all()
    res_data = SponsorSerializer(Sponsors, many = True, context={'request': request}).data

    if len(Sponsors):
        res_message = "Sponsors Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Sponsors Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)
 