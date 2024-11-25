from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration, name='registration'),
    path('login/', views.login_jwt, name='login'),
    path('get_user_by_jwt/', views.get_user_by_jwt, name='get_user_by_jwt'),
    path('login_teacher/', views.login_for_teacher, name='login_for_teacher')
]