from django.shortcuts import render
from .models import Mentor
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json

#view to get overall team data
@api_view(['POST'])
def mentorLogin(request):
    data = json.loads(request.body.decode("utf-8"))
    username = data['username']
    password = data['password']
    print(username, password)
    try:
        user = Mentor.objects.get(username = username)
        if user.password != password:
            res_message = "Invalid Password"
            res_status = status.HTTP_403_FORBIDDEN
        
        else:
            res_message = "Valid User"
            res_status = status.HTTP_200_OK

    except:
        res_message = "User Not Found"
        res_status = status.HTTP_403_FORBIDDEN
    

    return Response({
        "status_message": res_message,
        "status_code": res_status,
    }, status=res_status)
    
@api_view(['POST'])
def mentorLogout(request):
    logout(request)
