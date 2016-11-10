from django import forms
from django.contrib.auth import authenticate

from .models import *

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['title', 'tags']

	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
	first_message = forms.CharField(widget=forms.Textarea)

class MailForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['title', 'private_viewers']

	private_viewers = forms.ModelMultipleChoiceField(queryset=User.objects.all())
	first_message = forms.CharField(widget=forms.Textarea)

class NewMessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['content']

	content = forms.CharField(label="New message", widget=forms.Textarea)

class EditMessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['content']

	content = forms.CharField(label="Edit message", widget=forms.Textarea)
