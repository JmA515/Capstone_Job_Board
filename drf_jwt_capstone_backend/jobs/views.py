from functools import partial
from django.shortcuts import render
from rest_framework import status
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, AllowAny
from rest_framework.decorators import api_view, permission_classes
from .models import Job
from .serializers import JobSerializer
from django.contrib.auth import get_user_model
User = get_user_model()
from django.core.mail import send_mail
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
    # jobs = Job.objects.filter(status='available')
    serializer = JobSerializer(jobs, many=True)
    return Response(serializer.data)

@api_view(['POST', 'GET'])
@permission_classes([IsAuthenticated])
def user_jobs(request):
    logged_in_user = request.user
    user_logged_in = User.objects.get(id=logged_in_user.id)

    if request.method == 'POST':
        creator_id = user_logged_in
        title = request.data.get('title')
        description = request.data.get('description')
        status = request.data.get('status')
        post_date = request.data.get('post_date')
        lat_lng = user_logged_in.lat_lng
        new_job = Job(job_creator=creator_id, title=title, description=description, status=status, post_date=post_date, lat_lng=lat_lng)
        new_job.save()
        serializer = JobSerializer(data=new_job)
        send_mail(
            'Job Creation',
            (title + " job successfully created."),
            'noreply@goodneighbor.com',
            [logged_in_user.email],
            fail_silently=False,
        )
        if serializer.is_valid():
            serializer.save(job_creator=request.user)
            return Response(serializer.data, status=status.HTTP_201_CREATED)
        return Response(serializer.errors)
    elif request.method == 'GET':
        if request.GET.get('status') != None:
            jobs = Job.objects.filter(status=request.GET.get('status'))
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)
        else:
            jobs = Job.objects.filter(job_creator_id=request.user.id)
            serializer = JobSerializer(jobs, many=True)
            return Response(serializer.data)

@api_view(['PATCH'])
@permission_classes([IsAuthenticated])
def accept_user_job(request, job_pk):
    job = Job.objects.get(id = job_pk)
 
    updated_job = JobSerializer(job, data=request.data, partial=True)
    if updated_job.is_valid():
        updated_job.save()
        edited_job = Job.objects.get(id = job_pk)
        # print(edited_job.job_creator_id)
        creator = User.objects.get(id=edited_job.job_creator_id)
        # print("Accepted job that was created by " + creator.first_name)
        # print(edited_job.status)
        # print(edited_job.job_accepter)
        accepter = User.objects.get(id=edited_job.job_accepter)

        if (edited_job.status == "accepted"):
            send_mail(
                'Job Accepted',
                # (job.title + " job was accepted by "+ accepter.first_name + " " + accepter.last_name + "."),
                ("Your job, " + edited_job.title + " was accepted by " + accepter.first_name + " " + accepter.last_name + "."),
                'noreply@goodneighbor.com',
                [creator.email],
                fail_silently=False,
            )
        elif (edited_job.status == "completed"):
            send_mail(
                'Job Completed',
                ("Your job, " + edited_job.title + " was completed."),
                'noreply@goodneighbor.com',
                [creator.email],
                fail_silently=False,
            )
        return Response(updated_job.data)
    else:
        return Response(updated_job.errors)