from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import RequestConfig
from django.contrib.auth import authenticate, login, logout

import datetime

from .models import *
from .tables import *
from .forms import *

import random


def get_rand_pictures():
	return [
		random.choice([('/static/PgkkRd4.jpg',0,340)]),
		random.choice(['/static/took_u_long_enough___by_callergi-d8wdu85.jpg','/static/hengsha_morning_by_najtkriss-d4aelk1.jpg']),
	]


def _render(request, template, extra):
	extra['rand_pictures'] = get_rand_pictures()
	extra['signed_in_user'] = request.user.username if request.user.is_authenticated() else None
	return render(request, template, extra)


def sign_in(request):
	if request.method == 'POST':
		form = SignInForm(request.POST)
		if form.is_valid():
			user = authenticate(username=form.cleaned_data['username'], password=form.cleaned_data['password'])
			login(request, user)
			return redirect(request.POST['next'])
	else:
		form = SignInForm()
	return _render(request, 'forum/sign_in.html', {
		'form': form,
		'next': request.POST['next'] if 'next' in request.POST else (request.GET['next'] if 'next' in request.GET else '/'),
	})


def sign_out(request):
	logout(request)
	return redirect(request.GET['next'] if 'next' in request.GET else '/')


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


def tag(request, pk):
	tag = get_object_or_404(Tag.objects.all(), pk=pk)
	topics = Topic.objects.filter(tags__id__exact=tag.id).order_by('created').reverse()

	return _render(request, 'forum/tag.html', {
		'tag': tag,
		'topics': topics,
	})


def new_topic(request):
	if request.method == 'POST':
		form = TopicForm(request.POST)
		if form.is_valid():
			form.instance.author = request.user
			form.instance.save()
			first_message = Message(topic=form.instance, author=request.user, content=form.cleaned_data['first_message'])
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
	topic = get_object_or_404(Topic.objects.all(), pk=pk)
	messages = Message.objects.filter(topic=topic).order_by('posted')

	if edit_message:
		msgid = int(edit_message)
		pos = 0
		for message in messages:
			if message.pk == msgid:
				break
			pos += 1
		page = pos // 10 + 1

	page = int(page)
	num_pages = len(messages) // 10 + 1

	try:
		display_messages = messages[(page-1)*10:page*10]
	except:
		try:
			display_messages = messages[(page-1)*10:]
		except:
			display_messages = []

	edit_message_pk = None
	edit_message_form = None

	new_message_form = NewMessageForm()

	if request.method == 'GET':
		if edit_message:
			edit_message = messages.filter(pk=edit_message)
			if edit_message:
				edit_message = edit_message[0]
				if edit_message.author == request.user or request.user.has_perm('forum.edit_not_owned_message'):
					edit_message_pk = edit_message.pk
					edit_message_form = EditMessageForm({'content': edit_message.content})
					new_message_form = None

	else:
		if 'edit_message_pk' in request.POST:
			edit_message_form = EditMessageForm(request.POST)
			if edit_message_form.is_valid():
				message = messages.filter(pk=request.POST['edit_message_pk'])
				if message:
					message = message[0]
					if message.author == request.user or request.user.has_perm('forum.edit_not_owned_message'):
						message.content = edit_message_form.cleaned_data['content']
						message.edited = datetime.datetime.now()
						message.save()
						edit_message_form = None
			return redirect('topic', pk=topic.pk, page=request.POST['page'])

		else:
			new_message_form = NewMessageForm(request.POST)
			if new_message_form.is_valid():
				new_message_form.instance.author = request.user
				new_message_form.instance.topic = topic
				new_message_form.instance.save()
				new_message_form = NewMessageForm()
				return redirect('topic', pk=topic.pk, page=request.POST['page'])

	return _render(request, 'forum/topic.html', {
		'topic': topic,
		'messages': display_messages,
		'page': page,
		'num_pages': range(1, num_pages + 1),
		'new_message_form': new_message_form,
		'edit_message_pk': edit_message_pk,
		'edit_message_form': edit_message_form,
		'signed_in_user_can_edit_all': request.user.has_perm('forum.edit_not_owned_message'),
	})


def user(request, pk):
	user = get_object_or_404(User.objects.all(), pk=pk)

	return _render(request, 'forum/user.html', {
		'user': user,
	})

