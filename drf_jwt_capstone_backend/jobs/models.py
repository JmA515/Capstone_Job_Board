from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Job(models.Model):
    job_creator = models.ForeignKey(User, on_delete=models.CASCADE)
    job_accepter = models.IntegerField(null=True, blank=True)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=9) 
    post_date = models.DateField()
    lat_lng = models.CharField(max_length=100, null=True, blank=True)
