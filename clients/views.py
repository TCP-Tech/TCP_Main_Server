from django.shortcuts import render
from .models import *
from .serializers import *
from rest_framework import status
from django.contrib.auth import authenticate, login, logout
from rest_framework.decorators import api_view
from rest_framework.response import Response
import json
from rest_framework_simplejwt.tokens import RefreshToken
from django.contrib.auth.hashers import check_password
from rest_framework.decorators import authentication_classes, permission_classes
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework.permissions import IsAuthenticated
from django.views.decorators.csrf import csrf_exempt


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def logout_view(request):
    try:
        # Get the refresh token from the request
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'status_message': 'Refresh token is required',
                'status_code': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Create a RefreshToken instance and blacklist it
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            'status_message': 'Successfully logged out',
            'status_code': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status_message': 'Invalid or expired token',
            'status_code': status.HTTP_400_BAD_REQUEST,
        }, status=status.HTTP_400_BAD_REQUEST)

#view to get overall team data
@api_view(['POST'])
def mentorLogin(request):
    req = json.loads(request.body.decode("utf-8"))
    email = req['email']
    password = req['password']
    
    try:
        mentor = Mentor.objects.get(email=email)
        
        if not mentor.check_password(password):
            return Response({
                "status_message": "Invalid Password",
                "status_code": status.HTTP_403_FORBIDDEN,
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Create JWT tokens
        refresh = RefreshToken()
        refresh['user_id'] = mentor.id
        refresh['user_type'] = 'mentor'
        refresh['email'] = mentor.email
        
        return Response({
            "user_data": MentorSerializer(mentor).data,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "status_message": "Valid User",
            "status_code": status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
        
    except Mentor.DoesNotExist:
        return Response({
            "status_message": "User Not Found",
            "status_code": status.HTTP_403_FORBIDDEN,
        }, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def mentor_logout(request):
    try:
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'status_message': 'Refresh token is required',
                'status_code': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        
        return Response({
            'status_message': 'Mentor successfully logged out',
            'status_code': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status_message': 'Invalid or expired token',
            'status_code': status.HTTP_400_BAD_REQUEST,
        }, status=status.HTTP_400_BAD_REQUEST)

    
@api_view(['POST'])
def menteeLogin(request):
    req = json.loads(request.body.decode("utf-8"))
    email = req['email']
    password = req['password']
    
    try:
        mentee = Mentee.objects.get(email=email)
        
        if not mentee.check_password(password):
            return Response({
                "status_message": "Invalid Password",
                "status_code": status.HTTP_403_FORBIDDEN,
            }, status=status.HTTP_403_FORBIDDEN)
        
        # Create JWT tokens
        refresh = RefreshToken()
        refresh['user_id'] = mentee.id
        refresh['user_type'] = 'mentee'
        refresh['email'] = mentee.email
        
        return Response({
            "user_data": MenteeSerializer(mentee).data,
            "access_token": str(refresh.access_token),
            "refresh_token": str(refresh),
            "status_message": "Valid User",
            "status_code": status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
        
    except Mentee.DoesNotExist:
        return Response({
            "status_message": "User Not Found",
            "status_code": status.HTTP_403_FORBIDDEN,
        }, status=status.HTTP_403_FORBIDDEN)
    
@api_view(['POST'])
def menteeRegister(request):
    # try:
        data = request.data.copy()
        mentorEmail = data.get('mentor_email')
        mentor = Mentor.objects.get(email=mentorEmail)  # Get the mentor object
        mentorid=mentor.id
        data['mentor_id'] = mentor.id  # Use the mentor's ID
        data.pop('mentor_email', None)  # Remove 'mentor_email' from data
        serializer = MenteeSerializer(data=data)
        
        if serializer.is_valid():
            res_message = "Mentee created"
            res_status = status.HTTP_200_OK
            serializer.save() 
            if mentor.Mentorteam :
                # add this new mentee to  Mentorteam 
                mentee_instance = serializer.instance
                mentor.Mentorteam.team_members.add(mentee_instance)
                res_message += " and added to MentorTeam"
                mentee_instance.Menteeteam=mentor.Mentorteam
                mentee_instance.save()

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
            
    # except Exception as e:
    #     res_message = "Mentee couldn't be created"
    #     res_status = status.HTTP_403_FORBIDDEN
    #     return Response(
    #         {
    #                 "status_message": res_message,
    #                 "status_code": res_status,
    #             }, status=res_status
    #     )


@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def mentee_logout(request):
    try:
        refresh_token = request.data.get('refresh_token')
        
        if not refresh_token:
            return Response({
                'status_message': 'Refresh token is required',
                'status_code': status.HTTP_400_BAD_REQUEST,
            }, status=status.HTTP_400_BAD_REQUEST)
        
        # Blacklist the refresh token
        token = RefreshToken(refresh_token)
        token.blacklist()
        
        return Response({
            'status_message': 'Mentee successfully logged out',
            'status_code': status.HTTP_200_OK,
        }, status=status.HTTP_200_OK)
        
    except Exception as e:
        return Response({
            'status_message': 'Invalid or expired token',
            'status_code': status.HTTP_400_BAD_REQUEST,
        }, status=status.HTTP_400_BAD_REQUEST)
    
@api_view(['POST'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateMentorProfile(request):
    # try:
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def updateMenteeProfile(request):
    # try:
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
def get_team_mentee(request,id):
    try:
        mentee = Mentee.objects.get(id=id)
        if mentee:
            team_data = mentee.get_team()
            mentor = team_data[0].alloted_mentor
            mentorSerializer = MentorGetSerializer(mentor)
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
    res_data = MenteeGetSerializer(Mente, many=True, context={'request': request}).data
 
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
            mentor.Mentorteam=team
            mentor.save()
               
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
@authentication_classes([JWTAuthentication])
@permission_classes([IsAuthenticated])
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
    

