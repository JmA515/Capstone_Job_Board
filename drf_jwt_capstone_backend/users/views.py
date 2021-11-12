from django.shortcuts import render
from authentication.models import User 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
import json
from authentication.serializers import RegistrationSerializer
from ratings.models import Rating


# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile(request):
    logged_in_user = request.user
    user_logged_in = User.objects.get(id=logged_in_user.id)
    print(user_logged_in.first_name)
    print(request.data)
    print(request.data.get('email'))

    if request.method == "POST":
        # print(json.loads(request.body.decode('utf-8')))
        # body = json.loads(request.body.decode('utf-8'))
        # user_logged_in.first_name = body['first_name']
        # user_logged_in.last_name = body['last_name']
        # user_logged_in.address = body['address']
        # user_logged_in.zip_code = body['zip_code']
        user_logged_in.email = request.data.get('email')
        user_logged_in.first_name = request.data.get('first_name')
        user_logged_in.last_name = request.data.get('last_name')
        user_logged_in.address = request.data.get('address')
        user_logged_in.zip_code = request.data.get('zip_code')
        user_logged_in.save()
        serializer = RegistrationSerializer(user_logged_in)
        print(user_logged_in.email)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        serializer = RegistrationSerializer(user_logged_in)
        return Response(serializer.data, status=status.HTTP_200_OK)

@api_view(['PATCH', 'GET'])
@permission_classes([IsAuthenticated])
def rate_user(request, user_pk):
    user = User.objects.get(id = user_pk)
    if request.method == 'GET':
        serializer = RegistrationSerializer(user)
        return Response(serializer.data, status=status.HTTP_200_OK)
    elif request.method == 'PATCH':
        updated_user = RegistrationSerializer(user, data=request.data, partial=True)
        if updated_user.is_valid():
            updated_user.save()
            return Response(updated_user.data)
        else:
            return Response(updated_user.errors)
    
# @api_view(['GET'])
# @permission_classes([AllowAny])
# def get_user_rating(request, user_pk):
#     user = Rating.objects.get(id = user_pk)
#     if request.method == 'GET':
#         serializer = RegistrationSerializer(user)
#         return Response(serializer.data, status=status.HTTP_200_OK)
