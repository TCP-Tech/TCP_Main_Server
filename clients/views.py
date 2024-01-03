from django.shortcuts import render
from .models import Mentor
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response

#view to get overall team data
@api_view(['POST'])
def mentorLogin(request):
    username = request.POST.get('username')
    password = request.POST.get('password')

    try:
        user = Mentor.objects.get(username = username)
        
        if user.password != password:
            res_message = "Invalid Password"
            res_status = status.HTTP_403_FORBIDDEN
        
        else:
            login(request, user)
            res_message = "Valid User"
            res_status = status.HTTP_200_OK

    except:
        res_message = "User Not Found"
        res_status = status.HTTP_403_FORBIDDEN
    

    return Response({
        "message": res_message,
    }, status=res_status)
    
@api_view(['POST'])
def mentorLogout(request):
    logout(request)
