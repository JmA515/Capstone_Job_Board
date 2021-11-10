from django.urls import path
from jobs import views

urlpatterns = [
    # path('', views.JobList.as_view())
    path('all/', views.get_all_jobs),
    path('accept/<int:job_pk>/', views.accept_user_job),
    path('', views.user_jobs),
    
]