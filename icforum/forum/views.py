from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig

from .models import *
from .tables import *

def home(request):
	tags = Tag.objects.filter(main=True)

	return render(request, 'forum/home.html', {
		'tags': tags,
	})

def tag(request, pk):
	tag = get_object_or_404(Tag.objects.all(), pk=pk)
	topics = Topic.objects.filter(tags__id__exact=tag.id).order_by('created').reverse()

	return render(request, 'forum/tag.html', {
		'tag': tag,
		'topics': topics,
	})

def topic(request, pk):
	topic = get_object_or_404(Topic.objects.all(), pk=pk)
	messages = Message.objects.filter(topic=topic).order_by('posted')

	return render(request, 'forum/topic.html', {
		'topic': topic,
		'messages': messages,
	})

def user(request, pk):
	user = get_object_or_404(User.objects.all(), pk=pk)

	return render(request, 'forum/user.html', {
		'user': user,
	})

