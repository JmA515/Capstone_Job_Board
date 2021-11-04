from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .models import Job
from .serializers import JobSerializer
from django.contrib.auth.models import User

# Create your views here.

# class JobList(APIView):

#     permission_classes = [AllowAny]

#     def get(self, request):
#         jobs = Job.objects.all()
#         serializer = JobSerializer(jobs, many=True)
#         return Response(serializer.data)

@api_view(['GET'])
@permission_classes([AllowAny])
def get_all_jobs(request):
    jobs = Job.objects.all()
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def user_jobs(request):

    print('User', f"{request.user.id} {request.user.email} {request.user.username}")

    if request.method == 'POST':
        serializer = JobSerializer(data=request.data)
        if serializer.is_valid():
            serializer.save(job_creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)
    elif request.method == 'GET':
        jobs = Job.objects.filter(job_creator_id=request.user.id)
        serializer = JobSerializer(jobs, many=True)
        return Response(serializer.data)