from django.db import models
from django.contrib.auth.models import User


# Create your models here.
class Job(models.Model):
    job_creater = models.ForeignKey('authentication.User', on_delete=models.CASCADE)
    title = models.CharField(max_length=30)
    description = models.CharField(max_length=200)
    status = models.CharField(max_length=9) 
    post_date = models.DateField()
