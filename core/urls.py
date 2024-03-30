from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.loginpage, name='login'), 
    path('logout/', views.logoutUser , name='logout'), 

    path('', views.home, name='home'), 
    path('create-room/', views.createRoom, name='create-room'),
    path('room/<str:pk>/', views.room, name='room'), 
    path('edit-room/<str:pk>/', views.updatedRoom, name='edit-room'),
    path('delete-room/<str:pk>/', views.deleteRoom, name='delete-room'),



]
