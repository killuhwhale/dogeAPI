from django.urls import path
from . import views

urlpatterns = [
    path('doge/', views.prices),
    path('tweets/', views.tweets),
]