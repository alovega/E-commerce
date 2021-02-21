from __future__ import unicode_literals

from django.contrib import admin
from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
	"""
	Admin for custom user model
	"""
	list_filter = ('date_joined',)
	list_display = ('first_name', 'last_name', 'username', 'email', 'is_staff', 'date_joined')
	ordering = ('-date_joined',)
	search_fields = ('email', 'username', 'last_name', 'first_name')
