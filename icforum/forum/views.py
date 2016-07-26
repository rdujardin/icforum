from django.shortcuts import render
from django.http import HttpResponse

from .models import *

def home(request):
	tags = Tag.objects.filter(main=True)

	return render(request, 'forum/home.html', {
		'ftags': tags,
	})

# def tag(request, pk):
# 	tag = Tag.objects.filter(pk=pk)
# 	topics = Topic.objects.filter(tags__contains=tag)

# 	return render(request, 'forum/tag.html', {
# 		'tag': tag,
# 		'topics': topics,
# 	})

