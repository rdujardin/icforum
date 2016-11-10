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

	return _render(request, 'files/list_files.html', {
		'files': display_files,
		'page': page,
		'num_pages': range(1, num_pages + 1),
	})

def file(request, pk):
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

	return _render(request, 'files/file.html', {
		'file': file,
		'chapters': chapters,
	})

def chapter(request, pk):
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

	# Render
	return _render(request, 'files/chapter.html', {
		'chapter': chapter,
	})