from django.db import models
from django.contrib.auth import get_user_model
User = get_user_model()

# Create your models here.
class Rating(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="user")
    job_satisfaction_rating = models.ForeignKey(User, on_delete=models.CASCADE, related_name="rating", db_column="job_satisfaction_rating", null=True, blank=True)
