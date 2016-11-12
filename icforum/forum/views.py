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
from .forms import *

import random
import bleach
from urllib.parse import urlparse

from users.common import sanitize_html, _render


def home(request):
	tags = Tag.objects.filter(main=True)

	for tag in tags:
		messages = Message.objects.filter(topic__tags__id__exact=tag.id).order_by('posted').reverse()
		if messages:
			tag.last_message = messages[0]
		else:
			tag.last_message = None

	return _render(request, 'forum/home.html', {
		'tags': tags,
	})


def tag(request, pk, page=1):
	tag = get_object_or_404(Tag.objects.all(), pk=pk)

	post_it_topics = Topic.objects.filter(tags__id__exact=tag.id, post_it=True).order_by('created')
	regular_topics = Topic.objects.filter(tags__id__exact=tag.id, post_it=False).order_by('created').reverse()

	if tag.only_for.all():
		allowed = False
		for allowed_group in tag.only_for.all():
			if allowed_group in request.user.groups.all():
				allowed = True

		if not allowed:
			return redirect(home)

	# Determine which page to display and how many pages exist in tag
	page = int(page)
	num_pages = len(regular_topics) // 10 + 1

	# Select the topics standing on the right page
	try:
		display_topics = regular_topics[(page-1)*10:page*10]
	except:
		try:
			display_topics = regular_topics[(page-1)*10:]
		except:
			display_topics = []

	def set_last_message(topic_set):
		for topic in topic_set:
			messages = Message.objects.filter(topic=topic).order_by('posted').reverse()
			if messages:
				topic.last_message = messages[0]
			else:
				topic.last_message = None

	set_last_message(post_it_topics)
	set_last_message(regular_topics)

	return _render(request, 'forum/tag.html', {
		'tag': tag,
		'post_it_topics': post_it_topics,
		'regular_topics': display_topics,
		'page': page,
		'num_pages': range(1, num_pages + 1),
	})


def mail(request, page=1):

	user = request.user
	if user.is_anonymous():
		return redirect(home)

	profile = get_object_or_404(Profile.objects.all(), user=user)

	topics = Topic.objects.filter(private_viewers__id=user.id).order_by('updated').reverse()

	# Determine which page to display and how many pages exist in tag
	page = int(page)
	num_pages = len(topics) // 10 + 1

	# Select the topics standing on the right page
	try:
		display_topics = topics[(page-1)*10:page*10]
	except:
		try:
			display_topics = topics[(page-1)*10:]
		except:
			display_topics = []

	return _render(request, 'forum/mail.html', {
		'user': user,
		'profile': profile,
		'topics': display_topics,
		'page': page,
		'num_pages': range(1, num_pages + 1),
	})


def new_mail(request, pk=0):
	if request.method == 'POST':
		form = MailForm(request.POST)
		if form.is_valid():
			form.instance.author = request.user
			form.instance.save()
			first_message = Message(topic=form.instance, author=request.user, content=sanitize_html(form.cleaned_data['first_message']))
			first_message.save()
			for viewer in form.cleaned_data['private_viewers']:
				form.instance.private_viewers.add(viewer)
			if not request.user in form.cleaned_data['private_viewers']:
				form.instance.private_viewers.add(request.user)
			return redirect(topic, pk=form.instance.pk)
	else:
		if pk != 0:
			form = MailForm({'private_viewers': pk})
		else:
			form = MailForm()

	return _render(request, 'forum/new_topic.html', {
		'form': form,
	})


def new_topic(request):
	if request.method == 'POST':
		form = TopicForm(request.POST)
		if form.is_valid():
			form.instance.author = request.user
			form.instance.save()
			first_message = Message(topic=form.instance, author=request.user, content=sanitize_html(form.cleaned_data['first_message']))
			first_message.save()
			for tag in form.cleaned_data['tags']:
				form.instance.tags.add(tag)
			return redirect(topic, pk=form.instance.pk)
	else:
		form = TopicForm()

	return _render(request, 'forum/new_topic.html', {
		'form': form,
	})


def topic(request, pk, edit_message=None, page=1):
	# Get topic
	topic = get_object_or_404(Topic.objects.all(), pk=pk)

	# Get tags
	tags = topic.tags.all()

	# Check that topic does not belong to a tag only for a group the signed in user does not belong to
	for tag in topic.tags.all():
		if tag.only_for.all():
			allowed = False
			for allowed_group in tag.only_for.all():
				if allowed_group in request.user.groups.all():
					allowed = True
			if not allowed:
				return redirect(home)

	# Check if the topic is public or if the user can see it
	private_viewers = topic.private_viewers.all()
	can_see = (not private_viewers) or request.user in private_viewers
	if not can_see:
		return redirect(home)

	# Get messages in topic
	messages = Message.objects.filter(topic=topic).order_by('posted')

	# If given a message id to edit, determine on which page it stands
	if edit_message:
		msgid = int(edit_message)
		pos = 0
		for message in messages:
			if message.pk == msgid:
				break
			pos += 1
		page = pos // 10 + 1

	# Determine which page to display and how many pages exist in topic
	page = int(page)
	num_pages = len(messages) // 10 + 1

	# Select the messages standing on the right page
	try:
		display_messages = messages[(page-1)*10:page*10]
	except:
		try:
			display_messages = messages[(page-1)*10:]
		except:
			display_messages = []

	# Determine if 'edited' date must be shown for each message
	for msg in display_messages:
		delta = msg.edited - msg.posted if msg.edited > msg.posted else msg.posted - msg.edited
		msg.show_edited = delta >= datetime.timedelta(seconds=1)

	# Some initialization
	edit_message_pk = None
	edit_message_form = None

	# Prepare new message form
	new_message_form = NewMessageForm()

	if request.method == 'GET':
		if edit_message:
			# If an edit link has been clicked, prepare edit message form and remove new message form
			edit_message = messages.filter(pk=edit_message)
			if edit_message:
				edit_message = edit_message[0]
				if edit_message.author == request.user or request.user.has_perm('forum.edit_not_owned_message'):
					edit_message_pk = edit_message.pk
					edit_message_form = EditMessageForm({'content': edit_message.content})
					new_message_form = None

	else:
		if 'edit_message_pk' in request.POST:
			# Edit message form submitted
			edit_message_form = EditMessageForm(request.POST)
			if edit_message_form.is_valid() and not topic.closed:
				message = messages.filter(pk=request.POST['edit_message_pk'])
				if message:
					message = message[0]
					if message.author == request.user or request.user.has_perm('forum.edit_not_owned_message'):
						message.content = sanitize_html(edit_message_form.cleaned_data['content'])
						message.edited = datetime.datetime.now()
						message.save()
						edit_message_form = None
			return redirect('topic', pk=topic.pk, page=request.POST['page'])

		else:
			# New message form submitted
			new_message_form = NewMessageForm(request.POST)
			if new_message_form.is_valid() and not topic.closed:
				new_message_form.instance.author = request.user
				new_message_form.instance.topic = topic
				new_message_form.instance.content = sanitize_html(new_message_form.instance.content)
				new_message_form.instance.save()
				new_message_form = NewMessageForm()
				return redirect('topic', pk=topic.pk, page=request.POST['page'])

	# Render
	return _render(request, 'forum/topic.html', {
		'topic': topic,
		'tags': tags,
		'private_viewers': private_viewers,
		'messages': display_messages,
		'page': page,
		'num_pages': range(1, num_pages + 1),
		'new_message_form': new_message_form,
		'edit_message_pk': edit_message_pk,
		'edit_message_form': edit_message_form,
		'signed_in_user_can_edit_all': request.user.has_perm('forum.edit_not_owned_message'),
	})
