from django.urls import path
from . import views

urlpatterns = [
    path('send_task/<int:task_id>/<int:user_id>/', views.send_task, name='send_task'),
    path('task_detail/<int:task_id>/', views.task_detail, name="task_detail"),
    path('list_tasks/', views.list_tasks, name='list_tasks'),
    path('list_sended_tasks/<int:task_id>/<int:user_id>/', views.list_sended_tasks, name='list_sended_tasks')
]
