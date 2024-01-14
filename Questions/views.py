from django.shortcuts import render
from .models import Question
from .serializers import QuestionSerializer
from rest_framework import status
from rest_framework.decorators import api_view
from rest_framework.response import Response
from django.utils import timezone
from clients.models import * 
import json


    
@api_view(['POST'])
def QuestionRegister(request):
    
    # try:
        data = request.data
        serializer = QuestionSerializer(data=data)

        if serializer.is_valid():
            serializer.save() 
            mentorId=data.get('mentorId')
            mentor=Mentor.objects.get(id=mentorId)
            mentees = Mentee.objects.filter(mentor_id__in=mentorId)
            for mentee in mentees:
                mentee.total_q+=1
                mentee.save()

            mentor.total_q+=1
            mentor.save()
            team=Team.objects.get(alloted_mentor=mentor)
            
            res_message = "Question added into DB"
            res_status = status.HTTP_200_OK
            return Response(
                {
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
        else:
            res_message = "Question Syntax Invalid"
            res_status = status.HTTP_403_FORBIDDEN
    
            return Response(
                {
                    "user_data": serializer.errors,
                    "status_message": res_message,
                    "status_code": res_status,
                }, status=res_status)
            
    # except Exception as e:
    #     res_message = "Question Processing error"
    #     res_status = status.HTTP_403_FORBIDDEN
    #     return Response(
    #         {
    #                 "status_message": res_message,
    #                 "status_code": res_status,
    #             }, status=res_status
    #     )

@api_view(['GET'])
def GetQuestion(request):
    data=request.data
    mentorId=data.get("mentorId")
    question = Question.objects.all().filter(mentorId = mentorId)
    res_data = QuestionSerializer(question, many = True, context={'request': request}).data
 
    if len(question):
        res_message = "questions Data Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "questions Data couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)

#function to calculate score

def getScore(allotedTime,submittedtime):
    allotedhour=allotedTime.hour 
    submithour=submittedtime.hour
    allotedday=allotedTime.day
    submitday=submittedtime.day

    hour_difference=(allotedhour -submithour)
    day_difference=(allotedday-submitday)
    if day_difference==0:
        if hour_difference<6:
            return 20
        elif hour_difference>6 and hour_difference<12:
            return 15
        elif hour_difference>12 and hour_difference<18 :
            return 10
        else:
            return 5
    else:
        return 5

    
    

@api_view(['POSt'])
def Onsubmit(request):
    data=request.data
    menteeId=data.get("menteeId")
    qId=data.get("qId")


    question=Question.objects.get(id=qId)

    if question:
        question.Qstatus=True
        question.SubmittedAt=timezone.now()
        question.save()
        res_msg="question successfullty submited"
        res_status = status.HTTP_200_OK

    else:
        res_message = "questions does not exist"
        res_status = status.HTTP_404_NOT_FOUND

    mentorId=question.mentorId
    mentor=Mentor.objects.get(id=mentorId)
    mentee=Mentee.objects.get(id=menteeId)
    team=Team.objects.get(team_members=mentee)
    
    score=getScore(question.allotedTime,question.SubmittedAt)
    mentor.score+=score
    mentee.score+=score
    team.team_score+=score
    team.save()
    mentor.save()
    mentee.save()

    
    return Response({
        "message": res_msg
    }, status=res_status)

