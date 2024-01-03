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
    req = json.loads(request.body.decode("utf-8"))
    username = req['username']
    password = req['password']
    data = {}
    user = Mentor.objects.get(username = username)
    try:
        if user.password != password:
            res_message = "Invalid Password"
            res_status = status.HTTP_403_FORBIDDEN
        
        else:
            res_message = "Valid User"
            res_status = status.HTTP_200_OK
            for k,v in user.__dict__.items():
                if str(k) == '_state':
                    continue
                data[k]=str(v)
    except:
        res_message = "User Not Found"
        res_status = status.HTTP_403_FORBIDDEN
    
    return Response({
        "user_data": data,
        "status_message": res_message,
        "status_code": res_status,
    }, status=res_status)
    
@api_view(['POST'])
def mentorLogout(request):
    logout(request)
