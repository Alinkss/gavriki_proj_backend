from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.registration, name='registration'),
    path('login/', views.login_jwt, name='login'),
    path('my_view', views.my_view, name='my_view'),
]