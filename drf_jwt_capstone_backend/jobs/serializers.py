from rest_framework import serializers
from .models import Job

class JobSerializer(serializers.ModelSerializer):
    class Meta:
        model = Job
        fields = ['id', 'job_creator_id', 'title', 'description', 'status', 'post_date', 'job_accepter', 'lat_lng']