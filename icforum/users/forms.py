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

class ChangeAvatarForm(forms.Form):
	avatar = forms.ImageField(label='Image file (max. 512 kb)')

	def clean_content(self):
		content = self.cleaned_data['content']
		content_type = content.content_type.split('/')[0]
		if content_type in settings.CONTENT_TYPES:
			if content.size > settings.MAX_UPLOAD_SIZE:
				raise forms.ValidationError('File is too big')
		else:
			raise forms.ValidationError('File type is not supported')
		return content