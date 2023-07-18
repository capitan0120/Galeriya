from django.urls import path
from .views import galeriya, viewPhoto, addPhoto, loginUser, logoutUser, registerUser

urlpatterns = [
    path('login/', loginUser, name="login"),
    path('logout/', logoutUser, name="logout"),
    path('register/', registerUser, name="register"),

    path('', galeriya, name='galeriya'),
    path('photo/<str:pk>/', viewPhoto, name='view-photo'),
    path('add/', addPhoto, name='add-photo'),
]
