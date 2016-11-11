from django import forms
from django.contrib.auth import authenticate

from .models import *

class NewFileForm(forms.ModelForm):
	class Meta:
		model = File
		fields = ['title', 'tags']

	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

class ChapterForm(forms.ModelForm):
	class Meta:
		model = Chapter
		fields = ['title', 'position', 'content']

	content = forms.CharField(label="Chapter content", widget=forms.Textarea)