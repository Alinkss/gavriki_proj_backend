from django import forms

class PlagiarismCheckForm(forms.Form):
    text = forms.CharField()