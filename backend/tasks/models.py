from django.db import models
from django.contrib.auth.models import User
from register.models import RegisterForTeacher

class Task(models.Model):
    teacher = models.ForeignKey(RegisterForTeacher, on_delete=models.CASCADE)
    title = models.CharField(max_length=300)
    content = models.CharField(max_length=3000)
    dedline = models.DateTimeField()
    published_date = models.DateTimeField(auto_now_add=True)
    sended = models.ManyToManyField(User, related_name='sended')
    
class StudentSendTask(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    text = models.CharField(max_length=6000)
    published_date = models.DateTimeField(auto_now_add=True)
    task = models.ForeignKey(Task, on_delete=models.CASCADE)
    published_date = models.DateTimeField(auto_now_add=True)
