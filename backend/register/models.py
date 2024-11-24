from django.db import models
from django.contrib.auth.models import User

class Register(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    fio = models.CharField(max_length=400)
    university_group = models.CharField(max_length=30)
    
    def __str__(self):
        return f"{self.fio}, {self.university_group}"
    
    
    

