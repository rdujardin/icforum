from django.contrib import admin

from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'signup_date']

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
	list_display = ['name', 'main']
	order_by = ['main']

@admin.register(Topic)
class TopicAdmin(admin.ModelAdmin):
	list_display = ['title', 'author', 'created', 'updated']
	order_by = ['updated']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
	list_display = ['topic', 'author', 'posted', 'edited']
	order_by = ['edited']
