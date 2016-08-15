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
			raise forms.ValidationError('Invalid username or password')
		else:
			profile = Profile.objects.get(user=user)
			if profile.banned:
				raise forms.ValidationError('You have been banned, try again later')

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

	content = forms.CharField(label="New message", widget=forms.Textarea)

class EditMessageForm(forms.ModelForm):
	class Meta:
		model = Message
		fields = ['content']

	content = forms.CharField(label="Edit message", widget=forms.Textarea)
