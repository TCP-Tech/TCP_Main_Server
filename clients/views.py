from django.shortcuts import render
from .models import *
from .serializers import *
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
    try:
        user = Mentor.objects.get(username = username)
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
        "status_message": res_message,
        "status_code": res_status,
    }, status=res_status)
    
    return Response({
        "user_data": data,
        "status_message": res_message,
        "status_code": res_status,
    }, status=res_status)
    
@api_view(['POST'])
def mentorLogout(request):
    logout(request)
    

@api_view(['POST'])
def menteeLogin(request):
    req = json.loads(request.body.decode("utf-8"))
    username = req['username']
    password = req['password']
    data = {}
    try:
        user = Mentee.objects.get(username = username)
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
        "status_message": res_message,
        "status_code": res_status,
    }, status=res_status)
    
    return Response({
        "user_data": data,
        "status_message": res_message,
        "status_code": res_status,
    }, status=res_status)
    
@api_view(['POST'])
def menteeRegister(request):
    req = json.loads(request.body.decode("utf-8"))
    try:
        data = req.data
        serializer = MenteeSerializer(data=data)
        
        if serializer.is_valid():
            res_message = "Mentee created"
            res_status = status.HTTP_200_OK
            serializer.save() 
            return Response(
                {
                    "user_data": serializer.data,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
        else:
            res_message = "User Not Found"
            res_status = status.HTTP_403_FORBIDDEN
    
            return Response(
                {
                    "user_data": serializer.errors,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
            
    except Exception as e:
        res_message = "User Not Found"
        res_status = status.HTTP_403_FORBIDDEN
        return Response(
            {
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status
        )


@api_view(['POST'])
def menteeLogout(request):
    logout(request)
    
@api_view(['GET'])
def get_team_mentor(request,id):
    try:
        mentor = Mentor.objects.get(id=id)
        if mentor:
            team_data = mentor.allotted_teams()
            data = {}
            k=0
            for team in team_data:
                
                mentee_ids = team.team_members.values_list('id', flat=True)
                mentees = Mentee.objects.filter(id__in=mentee_ids)
                menteeSerializer = MenteeSerializer(mentees, many=True)
                data[k]=menteeSerializer.data
                k+=1
            
            serializer = TeamSerializer(team_data, many=True)
            res_message = "Valid user"
            res_status = status.HTTP_200_OK
            return Response(
                    {
                            "team_data": serializer.data,
                            "mentee_data" : data,
                            "status_message": res_message,
                            "status_code": res_status,
                        }, status=res_status
                )
        else:
            res_message = "User  Not Found"
            res_status = status.HTTP_403_FORBIDDEN
    
            return Response(
                {
                    "user_data": serializer.errors,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
            
            
    except Exception as e:
        res_message = "Something went wrong"
        res_status = status.HTTP_403_FORBIDDEN
        return Response(
            {
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status
        )
    
@api_view(['GET'])
def get_team_mentee(request,id):
    try:
        mentee = Mentee.objects.get(id=id)
        if mentee:
            team_data = mentee.get_team()
            mentee_ids = team_data[0].team_members.values_list('id', flat=True)
            mentor = team_data[0].alloted_mentor
            mentorSerializer = MentorSerializer(mentor)
            mentees = Mentee.objects.filter(id__in=mentee_ids)
            serializer = MenteeSerializer(mentees, many=True)
            teamSerializer=TeamSerializer(team_data, many=True)

            res_message = "Valid user"
            res_status = status.HTTP_200_OK
            return Response(
                    {
                            "team_data":teamSerializer.data,
                            "mentor_data":mentorSerializer.data,
                            "mentee_data":serializer.data,
                            "status_message": res_message,
                            "status_code": res_status,
                        }, status=res_status
                )
        
        else:
            res_message = "User  Not Found"
            res_status = status.HTTP_403_FORBIDDEN
    
            return Response(
                {
                    "user_data": serializer.errors,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
            
    except Exception as e:
        res_message = "Something went wrong"
        res_status = status.HTTP_403_FORBIDDEN
        return Response(
            {
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status
        )