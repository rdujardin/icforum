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

class NewFileForm(forms.ModelForm):
	class Meta:
		model = File
		fields = ['title', 'tags']

	tags = forms.ModelMultipleChoiceField(queryset=Tag.objects.all())

class ChapterForm(forms.ModelForm):
	class Meta:
		model = Chapter
		fields = ['title', 'position', 'content']

	content = forms.CharField(label=_("Chapter content"), widget=forms.Textarea)