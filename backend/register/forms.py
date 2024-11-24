from django import forms
from django.contrib.auth.models import User
from django.contrib.auth.forms import UserCreationForm
from .models import Register

class UserRegister(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username','email', 'password',]
        
class RegisterForm(forms.ModelForm):
    class Meta:
        model = Register
        fields = ['fio', 'university_group',]
        
class LoginForm(forms.Form):
    username = forms.CharField(max_length=200)
    password = forms.CharField(max_length=200, widget=forms.PasswordInput)
        
