from django import forms
from django.contrib.auth import authenticate

from .models import *

class SignInForm(forms.Form):
	username = forms.CharField(max_length=100, label='Username')
	password = forms.CharField(max_length=100, label='Password', widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super(SignInForm, self).clean()
		user = authenticate(username=cleaned_data.get('username'), password=cleaned_data.get('password'))
		if user is None:
			raise ValidationError('Invalid username or password')

class TopicForm(forms.ModelForm):
	class Meta:
		model = Topic
		fields = ['title', 'tags']

	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())
	first_message = forms.CharField(widget=forms.Textarea)

class NewMessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['content']

	content = forms.CharField(widget=forms.Textarea)
