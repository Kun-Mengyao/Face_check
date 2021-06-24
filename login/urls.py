from django.urls import path

from . import views

urlpatterns = [
    path('register/', views.register),
    path('personalInfo/', views.personalInfo),
    path('picShow/', views.picShow),
    path('signIn/', views.signIn),
    path('faceCheck/', views.faceCheck)
]