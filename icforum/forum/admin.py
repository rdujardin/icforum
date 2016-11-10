from django.contrib import admin

from .models import *

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ['name', 'main']
	order_by = ['-main', 'name']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display = ['title', 'author', 'post_it', 'closed', 'created', 'updated']
	order_by = ['-post_it', 'closed', 'updated']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ['topic', 'author', 'posted', 'edited']
	order_by = ['edited']
