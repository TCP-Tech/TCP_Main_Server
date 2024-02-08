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
    email = req['email']
    password = req['password']
    data = {}
    try:
        user = Mentor.objects.get(email = email)
        if user.password != password:
            res_message = "Invalid Password"
            res_status = status.HTTP_403_FORBIDDEN
        
        else:
            res_message = "Valid User"
            res_status = status.HTTP_200_OK
            data=MentorSerializer(user).data
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
    email = req['email']
    password = req['password']
    data = {}
    try:
        user = Mentee.objects.get(email = email)
        if user.password != password:
            res_message = "Invalid Password"
            res_status = status.HTTP_403_FORBIDDEN
        
        else:
            res_message = "Valid User"
            res_status = status.HTTP_200_OK
            data=MenteeSerializer(user).data
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
    try:
        data = request.data
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
            res_message = "Mentee couldn't be created"
            res_status = status.HTTP_403_FORBIDDEN
    
            return Response(
                {
                    "user_data": serializer.errors,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
            
    except Exception as e:
        res_message = "Mentee couldn't be created"
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
    
@api_view(['POST'])
def updateMentorProfile(request):
    # try:
        req = json.loads(request.body.decode("utf-8"))
        mentor = Mentor.objects.get(email = request.data['email'])
        serializer = MentorUpdateSerializer(mentor,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res_message = "Profile updated"
            res_status = status.HTTP_200_OK
            return Response(
                {
                    "user_data": serializer.data,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
        else:
            res_message = "Profile couldn't be updated"
            res_status = status.HTTP_400_BAD_REQUEST
    
            return Response(
                {
                    "user_data": serializer.errors,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
            
    # except Exception as e:
    #     res_message = "Internal Server Error"
    #     res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    #     return Response(
    #         {
    #             "status_message": res_message,
    #             "status_code": res_status,
    #         }, status=res_status
    #     )

@api_view(['POST'])
def updateMenteeProfile(request):
    # try:
        req = json.loads(request.body.decode("utf-8"))
        mentee = Mentee.objects.get(email = request.data['email'])
        serializer = MenteeUpdateSerializer(mentee,data=request.data, partial=True)
        if serializer.is_valid():
            serializer.save()
            res_message = "Profile updated"
            res_status = status.HTTP_200_OK
            return Response(
                {
                    "user_data": serializer.data,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
        else:
            res_message = "Profile couldn't be updated"
            res_status = status.HTTP_400_BAD_REQUEST
    
            return Response(
                {
                    "user_data": serializer.errors,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
            
    # except Exception as e:
    #     res_message = "Internal Server Error"
    #     res_status = status.HTTP_500_INTERNAL_SERVER_ERROR
    #     return Response(
    #         {
    #             "status_message": res_message,
    #             "status_code": res_status,
    #         }, status=res_status
    #     )
    
@api_view(['GET'])
def get_team_mentor(request,id):
    try:
        mentor = Mentor.objects.get(id=id)
        if mentor:
            team_data = mentor.allotted_teams()            
            serializer = TeamSerializer(team_data, many=True)
            res_message = "Valid user"
            res_status = status.HTTP_200_OK
            return Response(
                    {
                            "team_data": serializer.data,
                            "status_message": res_message,
                            "status_code": res_status,
                        }, status=res_status
                )
        else:
            res_message = "Mentor Not Found"
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
            mentor = team_data[0].alloted_mentor
            mentorSerializer = MentorSerializer(mentor)
            teamSerializer=TeamSerializer(team_data, many=True)
            res_message = "Valid user"
            res_status = status.HTTP_200_OK
            return Response(
                    {
                            "team_data":teamSerializer.data,
                            "mentor_data":mentorSerializer.data,
                            "status_message": res_message,
                            "status_code": res_status,
                        }, status=res_status
                )
        
        else:
            res_message = "User  Not Found"
            res_status = status.HTTP_403_FORBIDDEN
    
            return Response(
                {
                    "user_data": teamSerializer.errors,
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
def Getteams(request):
    
    Teams = Team.objects.all()
    res_data = TeamSerializer(Teams, many = True, context={'request': request}).data
 
    if len(Teams):
        res_message = "Teams Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Team does not exist in DB"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data,
        "status_code": res_status
    }, status=res_status)

@api_view(['GET'])
def Getmentees(request):
    
    Mente = Mentee.objects.all()
    res_data = MenteeSerializer(Mente, many = True, context={'request': request}).data
 
    if len(Mente):
        res_message = "Mentees Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Mentee does not exist in DB"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data,
        "status_code": res_status
    }, status=res_status)

@api_view(['GET'])
def GetmenteeDetail(request,menteeId):
    
    Mente = Mentee.objects.get(id=menteeId)
    res_data = MenteeSerializer(Mente).data
 
    if Mente:
        res_message = "Mentee Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Mentee Does not exist in DB"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "data": res_data,
        "message": res_message,
        "status_code": res_status
    }, status=res_status)

@api_view(['GET'])
def GetmentorDetail(request,mentorId):
    
    Mento = Mentor.objects.get(id=mentorId)
    res_data = MentorSerializer(Mento).data
 
    if Mento:
        res_message = "Mentor Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Mentor Does not exist in DB"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "data": res_data,
        "message": res_message,
        "status_code": res_status
    }, status=res_status)

@api_view(['POST'])
def createTeam(request):
    teamname=request.data['teamname']
    mentorid=request.data['mentorid']
    
    mentor=Mentor.objects.get(id=mentorid)
    mentees=Mentee.objects.filter(mentor_id=mentorid)
    print(mentor)
    print(mentees)
    team = Team.objects.create(team_name=teamname, alloted_mentor=mentor)
    team.team_members.add(*mentees)   
    if team:
            res_message = "Team created"
            res_status = status.HTTP_200_OK
            team.save() 
            for mentee in mentees:
                mentee.Menteeteam=team
                mentee.save()
               
            return Response(
                {
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
    else:
            res_message = "Team couldn't be created"
            res_status = status.HTTP_403_FORBIDDEN
    
            return Response(
                {
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)

@api_view(['POST'])
def updateTeam(request):
    mentorid=request.data['mentorid']
    mentor=Mentor.objects.get(id=mentorid)
    team=Team.objects.get(alloted_mentor=mentor)
    data={
        'team_name':request.data['teamname']
    }
    serializer = TeamSerializer(team,data=data, partial=True)
    if serializer.is_valid():
            serializer.save()
            res_message = "team updated"
            res_status = status.HTTP_200_OK
            return Response(
                {
                    "user_data": serializer.data,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
    else:
            res_message = "team couldn't be updated"
            res_status = status.HTTP_400_BAD_REQUEST
    
            return Response(
                {
                    "user_data": serializer.errors,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
    

