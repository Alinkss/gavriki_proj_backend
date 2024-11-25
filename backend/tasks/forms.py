from django import forms
from tasks.models import Task, StudentSendTask

class SendTaskForm(forms.ModelForm):
    class Meta:
        model = StudentSendTask
        fields = ['text',]