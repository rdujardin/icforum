from django.contrib import admin

from .models import *

@admin.register(Profile)
class ProfileAdmin(admin.ModelAdmin):
	list_display = ['user', 'signup_date']
	order_by = ['-signup_date']