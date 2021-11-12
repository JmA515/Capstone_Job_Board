from django.urls import path
from users import views

urlpatterns = [
    path('profile/', views.profile),
    path('accept/<int:user_pk>/', views.rate_user),
    # path('profile/<int:user_pk>/', views.get_user_rating)
]
