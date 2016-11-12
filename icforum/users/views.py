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

from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.conf import settings
from django.utils import translation

import datetime

from .models import *
from .forms import *
from forum.views import home

import random

from users.common import sanitize_html, _render


def sign_in(request):
	if request.method == 'POST':
		form = SignInForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			login(request, user)
			return redirect(request.POST['next'])
	else:
		form = SignInForm()
	return _render(request, 'users/sign_in.html', {
		'form': form,
		'next': request.POST['next'] if 'next' in request.POST else (request.GET['next'] if 'next' in request.GET else '/'),
	})


def sign_out(request):
	logout(request)
	return redirect(request.GET['next'] if 'next' in request.GET else '/')


def user(request, pk):
	user = get_object_or_404(User.objects.all(), pk=pk)
	profile = Profile.objects.get(user=user)

	can_edit = user == request.user

	if request.method == 'POST':
		change_avatar_form = ChangeAvatarForm(request.POST, request.FILES)
		if change_avatar_form.is_valid() and can_edit:
			profile.avatar.save(change_avatar_form.cleaned_data['avatar'].name, change_avatar_form.cleaned_data['avatar'])
			change_avatar_form = ChangeAvatarForm()

	else:
		change_avatar_form = ChangeAvatarForm()

	return _render(request, 'users/user.html', {
		'user': user,
		'profile': profile,
		'can_edit': can_edit,
		'change_avatar_form': change_avatar_form,
	})


def set_language(request, lang):
	langs = ['en', 'fr']
	if lang in langs:
		print(lang)
		translation.activate(lang)
	return redirect(home)