from django.urls import path
from user_app.views import register, user_login, user_logout, manage_users, manage_trainers, manage_profile, users

urlpatterns = [
    path('register/', register, name='register'),
    path('login/', user_login, name='login'),
    path('logout/', user_logout, name='logout'),

    path('users/', users, name='users'),

    path('manage_profile/', manage_profile, name='manage_profile'),

    path('manage/<int:pk>/', manage_users, name='manage'),
    path('manage/trainers/<int:pk>/', manage_trainers, name='trainers')
]