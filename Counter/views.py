from django.shortcuts import render
from rest_framework.decorators import api_view
from .models import Counter
from .serializers import CounterSerializer
from rest_framework import status
from rest_framework.response import Response

    
#view to set timer
@api_view(['POST'])
def startTimer(request):
    data = request.data
    
    serializer = CounterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response({}, status=status.HTTP_200_OK)
    else:
        return Response({}, status=status.HTTP_404_NOT_FOUND)


#view to get startTime
@api_view(['GET'])
def getStartTime(request):
    time = Counter.objects.all()

    if len(time):
        res_data = CounterSerializer(time, many = True, context={'request': request}).data
        res_message = "Counter Already Started."
        res_status = status.HTTP_200_OK
    
    else:
        res_data = {"flag" : False, "startTime" : 0, "endTime" : 0}
        res_message = "Counter Not Started."
        res_status = status.HTTP_200_OK
    
    return Response({
        "message" : res_message,
        "data" : res_data
    }, status = res_status)