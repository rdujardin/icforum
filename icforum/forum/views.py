from django.shortcuts import render, get_object_or_404
from django_tables2 import RequestConfig

from .models import *
from .tables import *

def home(request):
	tags = Tag.objects.filter(main=True)
	tags_table = TagTable(tags)

	return render(request, 'forum/home.html', {
		'tags_table': tags_table,
	})

def tag(request, pk):
	tag = get_object_or_404(Tag.objects.all(), pk=pk)
	topics = Topic.objects.filter(tags__id__exact=tag.id).order_by('created').reverse()
	topics_table = TopicTable(topics)

	return render(request, 'forum/tag.html', {
		'tag': tag,
		'topics_table': topics_table,
	})

def topic(request, pk):
	topic = get_object_or_404(Topic.objects.all(), pk=pk)
	messages = Message.objects.filter(topic=topic).order_by('posted')
	messages_table = MessageTable(messages)

	return render(request, 'forum/topic.html', {
		'topic': topic,
		'messages_table': messages_table,
	})

def user(request, pk):
	user = get_object_or_404(User.objects.all(), pk=pk)

	return render(request, 'forum/user.html', {
		'user': user,
	})

