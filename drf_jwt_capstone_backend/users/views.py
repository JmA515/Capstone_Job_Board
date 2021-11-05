from django.shortcuts import render
from authentication.models import User 
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
import json
from authentication.serializers import RegistrationSerializer


# Create your views here.

@api_view(['GET', 'POST'])
@permission_classes([IsAuthenticated])
def profile(request):
    logged_in_user = request.user
    user_logged_in = User.objects.get(id=logged_in_user.id)

    if request.method == "POST":
        print(json.loads(request.body.decode('utf-8')))
        body = json.loads(request.body.decode('utf-8'))
        user_logged_in.first_name = body['first_name']
        user_logged_in.last_name = body['last_name']
        user_logged_in.address = body['address']
        user_logged_in.zip_code = body['zip_code']
        user_logged_in.save()
        serializer = RegistrationSerializer(user_logged_in)
        return Response(serializer.data, status=status.HTTP_200_OK)

    elif request.method == 'GET':
        serializer = RegistrationSerializer(user_logged_in)
        return Response(serializer.data, status=status.HTTP_200_OK)
