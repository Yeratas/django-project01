from . import views
from django.urls import path

urlpatterns = [
    path('', views.home, name='home'),
    path('login/', views.loginPage, name = 'login'),
    path('logout/', views.logoutPage, name = 'logout'),
    path('register/', views.registerUser, name = 'register'),
    path('profile/<str:id>/', views.userProfile, name='user_profile'),
    path('room/<str:id>/', views.rooms, name='room'),
    path('create_room/', views.create_room, name='create_room'),
    path('update_room/<str:pk>/', views.update_room, name='update_room'),
    path('delete_room/<str:pk>/', views.delete_room, name='delete_room'),
    path('delete_message/<str:pk>/', views.delete_message, name='delete_message'),

]