from django.shortcuts import render
from .models import TeamData
from .serializers import TeamDataSerializer
from rest_framework.decorators import api_view
from rest_framework.response import Response

#view to get overall team data
@api_view(['GET'])
def teamData(request):
    teammembers = TeamData.objects.all()
    rtr = TeamDataSerializer(teammembers, many = True)
    return Response(rtr.data)

#view to get each year's team data
@api_view(['GET'])
def teamDataByYear(request, year):
    teammembers = TeamData.objects.all().filter(year = year)
    rtr = TeamDataSerializer(teammembers, many = True)
    return Response(rtr.data)

