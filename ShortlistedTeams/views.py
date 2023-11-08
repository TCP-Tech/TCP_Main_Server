from django.shortcuts import render
from .models import ShortlistedTeam
from .serializers import ShortlistedTeamSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


#view to get ShortlistedTeams by year
@api_view(['GET'])
def ShortlistedTeamDataByYear(request, year):
    ShortlistedTeams = ShortlistedTeam.objects.all().filter(year = year)
    res_data = ShortlistedTeamSerializer(ShortlistedTeams, many = True, context={'request': request}).data
 
    if len(ShortlistedTeams):
        res_message = "ShortlistedTeams Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "ShortlistedTeams Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)

#view to get ShortlistedTeams 
@api_view(['GET'])
def ShortlistedTeamData(request):
    ShortlistedTeams = ShortlistedTeam.objects.all()
    res_data = ShortlistedTeamSerializer(ShortlistedTeams, many = True, context={'request': request}).data

    if len(ShortlistedTeams):
        res_message = "ShortlistedTeams Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "ShortlistedTeams Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)
 