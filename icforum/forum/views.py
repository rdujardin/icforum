from django.shortcuts import render, get_object_or_404, redirect
from django_tables2 import RequestConfig
from django.contrib.auth import authenticate, login, logout

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

def topic(request, pk):
	topic = get_object_or_404(Topic.objects.all(), pk=pk)
	messages = Message.objects.filter(topic=topic).order_by('posted')

	return _render(request, 'forum/topic.html', {
		'topic': topic,
		'messages': messages,
	})

def user(request, pk):
	user = get_object_or_404(User.objects.all(), pk=pk)

	return _render(request, 'forum/user.html', {
		'user': user,
	})

