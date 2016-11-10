from django.contrib import admin

from .models import *

@admin.register(File)
class FileAdmin(admin.ModelAdmin):
	list_display = ['title', 'created', 'updated']
	order_by = ['updated']

@admin.register(Chapter)
class ChapterAdmin(admin.ModelAdmin):
	list_display = ['file', 'position', 'title']
	order_by = ['file']
