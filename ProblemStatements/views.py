from django.shortcuts import render
from .models import ProblemStatement
from .serializers import ProblemStatementSerializer
from rest_framework.decorators import api_view
from rest_framework import status
from rest_framework.response import Response


#view to get problem statements by year
@api_view(['GET'])
def problemStatementDataByYear(request, year):
    problemStatements = ProblemStatement.objects.all().filter(year = year)
    res_data = ProblemStatementSerializer(problemStatements, many = True, context={'request': request}).data

    if len(problemStatements):
        res_message = "Problem Statements Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Problem Statements couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)

#view to get problem statements 
@api_view(['GET'])
def problemStatementData(request):
    problemStatements = ProblemStatement.objects.all()
    res_data = ProblemStatementSerializer(problemStatements, many = True, context={'request': request}).data

    if len(problemStatements):
        res_message = "Problem Statements Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Problem Statements couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND
    
    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)
 