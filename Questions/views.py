from django.shortcuts import render
from .models import Question
from .serializers import *
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
        level=data.get('Level')
        topicss=data.get('topic')
        topics=topicss.split(" ")

        
        serializer = addQuestionSerializer(data=data)
        

        if serializer.is_valid():
            serializer.save() 
            mentorId=data.get('mentorId')
            mentor=Mentor.objects.get(id=mentorId)
            mentees = Mentee.objects.filter(mentor_id__in=mentorId)
            for mentee in mentees:
                mentee.total_q+=1
                mentee.save()
            
            mentor.Qlevel_count[level]=mentor.Qlevel_count.get(level,0) + 1
            for topic in topics:
                mentor.topic_count[topic]=mentor.topic_count.get(topic,0) + 1
            mentor.total_q+=1
            mentor.save()
            team=Team.objects.get(alloted_mentor=mentor)
            
            res_message = "Question added to DB"
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
def GetQuestion(request,mentorId):
    
    question = Question.objects.all().filter(mentorId = mentorId)
    res_data = QuestionSerializer(question, many = True, context={'request': request}).data
 
    if len(question):
        res_message = "Question data fetched successfully"
        res_status = status.HTTP_200_OK
    else:
        res_message = "Question does not exist in DB"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        
        "data": res_data,
        "message": res_message,
        "status_code": res_status
    }, status=res_status)

#function to calculate score

def getScore(allotedTime,submittedtime):
    time_difference = submittedtime - allotedTime
    hours_difference = time_difference.total_seconds() // 3600
    days_difference = time_difference.days

    if days_difference == 0:
        if hours_difference < 6:
            return 20
        elif 6 <= hours_difference < 12:
            return 15
        elif 12 <= hours_difference < 18:
            return 10
        else:
            return 5
    else:
        return 5
    
#functions to calculate time difference
def getTimediff(allotedTime,submittedtime):
    time_difference = submittedtime - allotedTime
    return time_difference.total_seconds() // 60

def update_team_ranks():
    # Fetch all teams, order them by score (descending) and cumHour_diff (ascending)
    teams = Team.objects.all().order_by('-team_score', 'cumHour_diff')
    
    # Assign ranks based on the sorted order
    rank = 1
    for team in teams:
        team.team_rank = rank
        team.save()  # Save the updated rank
        rank += 1

    print("Team ranks updated successfully.")

def update_Mentee_ranks():
    # Fetch all teams, order them by score (descending) and cumHour_diff (ascending)
    mentees = Mentee.objects.all().order_by('-score', 'cumHour_diff')
    
    # Assign ranks based on the sorted order
    rank = 1
    for mentee in mentees:
        mentee.Mentee_rank = rank
        mentee.save()  # Save the updated rank
        rank += 1

    print("Mentee ranks updated successfully.")

@api_view(['POST'])
def Onsubmit(request):
    data=request.data
    
    menteeId=data.get("menteeId")
    qId=data.get("qId")
    mentee=Mentee.objects.get(id=menteeId)

    question=Question.objects.get(id=qId)
    level=question.Level
    topicss=question.topic
    topics=topicss.split(" ")

    

    menteesubmission=False
    
    if question.submitedMentees.exists():
        
        if mentee in question.submitedMentees.all():
            menteesubmission=True
       
    

    if question and not menteesubmission:
        question.Qstatus=True
        question.SubmittedAt=timezone.now()
        question.submitedMentees.add(mentee)
        question.save() 
        mentorId=question.mentorId
        mentor=Mentor.objects.get(id=mentorId)
        
        team=Team.objects.get(team_members=mentee)
        timediff=getTimediff(question.allotedTime,question.SubmittedAt)
        score=getScore(question.allotedTime,question.SubmittedAt)
        mentor.score+=score
        mentee.score+=score
        print(timediff)
        mentee.cumHour_diff += timediff
        mentee.solvedQ+=1
        mentee.Qlevel_count[level]=mentee.Qlevel_count.get(level,0) + 1
        for topic in topics:
            mentee.topic_count[topic]=mentee.topic_count.get(topic,0) + 1

        team.team_score+=score
        team.cumHour_diff += timediff
        team.save()
        mentor.save()
        mentee.save()
        update_team_ranks()
        update_Mentee_ranks()
        res_msg="Question submitted successfully"
        res_status = status.HTTP_200_OK
    
    elif menteesubmission:
        res_msg = "Question already submitted"
        res_status = status.HTTP_403_FORBIDDEN
    else :
        res_msg = "Question does not exist"
        res_status = status.HTTP_404_NOT_FOUND

    return Response({
        "message": res_msg,
        "score":score,
        "status_code": res_status
    }, status=res_status)

