from __future__ import unicode_literals

from django.contrib import admin
from django.contrib.auth.admin import UserAdmin

from users.models import CustomUser


@admin.register(CustomUser)
class CustomUserAdmin(UserAdmin):
	"""Admin for User model"""
	admin_fieldsets = list(UserAdmin.fieldsets)
	admin_fieldsets[1] = (
		('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone_number')})
	)
	admin_fieldsets = tuple(admin_fieldsets)
	fieldsets = admin_fieldsets
	add_fieldsets = (
		(None, {
			'classes': ('wide',),
			'fields': ('username', 'password1', 'password2', 'email', 'phone_number', 'first_name', 'last_name'),
		}),
	)
