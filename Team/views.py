from django.views.decorators.csrf import csrf_exempt
import json
from .models import TeamMember
from rest_framework.response import Response
from django.http import HttpResponse
from rest_framework.decorators import api_view, authentication_classes, permission_classes
from rest_framework import status
from rest_framework.permissions import IsAdminUser
from rest_framework_simplejwt.authentication import JWTAuthentication
from .serializers import TeamSerializer



@api_view(['GET', ])
def get_members(request,year):
    members = TeamMember.objects.filter(year=year)
    res_data = TeamSerializer(members, many=True,context={
            'request': request}).data
    if len(members) > 0:
        res_message = "Team members Fetched successfully."
        res_status = status.HTTP_200_OK
    else:
        res_message = "Team members couldn't be fetched"
        res_status = status.HTTP_404_NOT_FOUND

    return Response({
        "message": res_message,
        "data": res_data
    }, status=res_status)


@api_view(['POST', 'PATCH'])
@authentication_classes([JWTAuthentication])
@permission_classes([IsAdminUser])
def create_or_update_member(request):
    """
    Create or update a TeamMember identified by email.
    Requires a valid admin JWT token in the Authorization header.
    POST and PATCH behave identically: upsert by email.
    Returns the serialised member and whether it was created or updated.
    """
    email = request.data.get('email', '').strip().lower() or None

    if email:
        member = TeamMember.objects.filter(email=email).first()
    else:
        member = None

    if member:
        serializer = TeamSerializer(member, data=request.data, partial=True)
        created = False
    else:
        serializer = TeamSerializer(data=request.data)
        created = True

    if serializer.is_valid():
        serializer.save()
        return Response(
            {
                "message": "Member created." if created else "Member updated.",
                "created": created,
                "data": serializer.data,
            },
            status=status.HTTP_201_CREATED if created else status.HTTP_200_OK,
        )

    return Response(
        {"message": "Validation error.", "errors": serializer.errors},
        status=status.HTTP_400_BAD_REQUEST,
    )


# @api_view(['GET'])
# def team_years(req):
#     years = Member.objects.values_list('year').distinct()
#     return Response({
#         'years': [x for x in years]
#     })