# Copyright 2016 Infinite Connection
# 
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
# 
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

from django import forms
from django.contrib.auth import authenticate
from django.utils.translation import ugettext_lazy as _

from .models import *

class SignInForm(forms.Form):
	username = forms.CharField(max_length=100, label=_('Username'))
	password = forms.CharField(max_length=100, label=_('Password'), widget=forms.PasswordInput)

	def clean(self):
		cleaned_data = super(SignInForm, self).clean()
		user = authenticate(username=cleaned_data.get('username'), password=cleaned_data.get('password'))
		if user is None:
			raise forms.ValidationError(_('Invalid username or password'))
		else:
			profile = Profile.objects.get(user=user)
			if profile.banned:
				raise forms.ValidationError(_('You have been banned, try again later'))

class ChangeAvatarForm(forms.Form):
	avatar = forms.ImageField(label=_('Image file (max. 512 kb)'))

	def clean_content(self):
		content = self.cleaned_data['content']
		content_type = content.content_type.split('/')[0]
		if content_type in settings.CONTENT_TYPES:
			if content.size > settings.MAX_UPLOAD_SIZE:
				raise forms.ValidationError(_('File is too big'))
		else:
			raise forms.ValidationError(_('File type is not supported'))
		return content