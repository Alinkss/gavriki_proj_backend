from django.db import models
from django.contrib.auth.models import User

class Register(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='user')
    fio = models.CharField(max_length=400)
    university_group = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.fio}, {self.university_group}"

class RegisterForTeacher(models.Model):
    username = models.CharField(max_length=100)
    fio = models.CharField(max_length=400)
    password = models.CharField(max_length=200)
    email = models.EmailField()
    
    def __str__(self):
        return f"{self.fio}"
    
    

