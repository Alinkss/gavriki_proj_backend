from django import forms
    
class TextForm(forms.Form):
    text = forms.CharField(max_length=3000, widget=forms.Textarea, label="Введите текст для проверки")