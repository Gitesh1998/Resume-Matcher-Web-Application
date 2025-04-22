from django import forms
from .models import Resume

class ResumeUploadForm(forms.ModelForm):
    class Meta:
        model = Resume
        fields = ['file']

class JobDescriptionForm(forms.Form):
    description = forms.CharField(widget=forms.Textarea, label='Job Description')
