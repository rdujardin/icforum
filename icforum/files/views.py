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
from django_tables2 import RequestConfig
from django.contrib.auth import authenticate, login, logout
from django.conf import settings

import datetime

from .models import *
from users.models import *
from forum.views import home
from .forms import *

import random
import bleach
from urllib.parse import urlparse

from users.common import sanitize_html, _render

from django.core.exceptions import ObjectDoesNotExist

def list_files(request, page=1):

	files = File.objects.all()
	not_allowed = []

	for file in files:
		for tag in file.tags.all():
			if tag.only_for.all():
				allowed = False
				for allowed_group in tag.only_for.all():
					if allowed_group in request.user.groups.all():
						allowed = True
				if not allowed:
					not_allowed.append(file.pk)

	files = files.exclude(pk__in=not_allowed)

	# Determine which page to display and how many pages exist
	page = int(page)
	num_pages = len(files) // 10 + 1

	# Select the topics standing on the right page
	try:
		display_files = files[(page-1)*10:page*10]
	except:
		try:
			display_files = files[(page-1)*10:]
		except:
			display_files = []

	# List tags for each file
	for file in display_files:
		file.list_tags = file.tags.all()

	# Determine if user can manage files
	can_manage = request.user.has_perm('files.create_edit_file')

	return _render(request, 'files/list_files.html', {
		'files': display_files,
		'page': page,
		'num_pages': range(1, num_pages + 1),
		'can_manage': can_manage,
	})

def new_file(request):
	if not request.user.has_perm('files.create_edit_file'):
		return redirect(list_files)

	if request.method == 'GET':
		new_file_form = NewFileForm()
	else:
		new_file_form = NewFileForm(request.POST)
		if new_file_form.is_valid():
			new_file_form.instance.save()
			for tag in new_file_form.cleaned_data['tags']:
				new_file_form.instance.tags.add(tag)
			return redirect(file, pk=new_file_form.instance.pk)

	return _render(request, 'files/new_file.html', {
		'new_file_form': new_file_form,
	})

def file(request, pk, new_chapter=0):
	file = get_object_or_404(File.objects.all(), pk=pk)

	chapters = Chapter.objects.filter(file__id__exact=file.id).order_by('position')

	for tag in file.tags.all():
		if tag.only_for.all():
			allowed = False
			for allowed_group in tag.only_for.all():
				if allowed_group in request.user.groups.all():
					allowed = True
			if not allowed:
				return redirect(home)

	# Determine if user can manage files
	can_manage = request.user.has_perm('files.create_edit_file')

	new_chapter_form = None
	if can_manage and new_chapter == '1':
		if request.method == 'GET':
			new_chapter_form = ChapterForm()
		else:
			new_chapter_form = ChapterForm(request.POST)
			if new_chapter_form.is_valid():
				new_chapter_form.instance.content = sanitize_html(new_chapter_form.cleaned_data['content'])
				new_chapter_form.instance.file = file
				new_chapter_form.instance.file.updated = datetime.datetime.now()
				new_chapter_form.instance.save()
				return redirect(chapter, new_chapter_form.instance.pk)

	return _render(request, 'files/file.html', {
		'file': file,
		'chapters': chapters,
		'can_manage': can_manage,
		'new_chapter_form': new_chapter_form,
	})

def chapter(request, pk, edit=0):
	chapter = get_object_or_404(Chapter.objects.all(), pk=pk)

	# Get tags
	tags = chapter.file.tags.all()

	# Check that topic does not belong to a tag only for a group the signed in user does not belong to
	for tag in tags:
		if tag.only_for.all():
			allowed = False
			for allowed_group in tag.only_for.all():
				if allowed_group in request.user.groups.all():
					allowed = True
			if not allowed:
				return redirect(home)

	# Get previous and next chapter
	try:
		previous_chapter = Chapter.objects.get(file=chapter.file, position=chapter.position - 1)
	except ObjectDoesNotExist:
		previous_chapter = None
	try :
		next_chapter = Chapter.objects.get(file=chapter.file, position=chapter.position + 1)
	except ObjectDoesNotExist:
		next_chapter = None

	# Determine if user can manage files
	can_manage = request.user.has_perm('files.create_edit_file')

	# Chapter edit form
	if edit == '1' and can_manage:
		if request.method == 'GET':
			edit_chapter_form = ChapterForm(instance=chapter)
		else:
			edit_chapter_form = ChapterForm(request.POST)
			if edit_chapter_form.is_valid():
				chapter.content = sanitize_html(edit_chapter_form.cleaned_data['content'])
				chapter.file.updated = datetime.datetime.now()
				chapter.save()
				edit_chapter_form = None
	else:
		edit_chapter_form = None

	# Render
	return _render(request, 'files/chapter.html', {
		'chapter': chapter,
		'previous_chapter': previous_chapter,
		'next_chapter': next_chapter,
		'can_manage': can_manage,
		'edit_chapter_form': edit_chapter_form,
	})
