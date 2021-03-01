# Register your models here.

from __future__ import unicode_literals

from django.contrib import admin
from sms.models import Outbox, DeliveryReport, Inbox


@admin.register(Outbox)
class OrderAdmin(admin.ModelAdmin):
	"""
	Admin for custom user model
	"""
	list_filter = ('date_created', 'status')
	list_display = ('id', 'status', 'statusCode', 'phone', 'text', 'messageId', 'date_created')
	ordering = ('-date_created',)
	search_fields = ('status', 'statusCode', 'phone', 'messageId')


@admin.register(Inbox)
class InboxAdmin(admin.ModelAdmin):
	"""
	Admin for custom user model
	"""
	list_filter = ('date_created',)
	list_display = ('id', 'text', 'phone', 'to', 'linkId', 'date_created')
	ordering = ('-date_created',)
	search_fields = ('phone', 'linkId')


@admin.register(DeliveryReport)
class DeliveryReportAdmin(admin.ModelAdmin):
	"""
	Admin for custom user model
	"""
	list_filter = ('date_created', 'date_modified', 'status')
	list_display = ('id', 'identifier', 'status', 'networkCode', 'date_created', 'date_modified')
	ordering = ('-date_created',)
	search_fields = ('status', 'identifier', 'networkCode')
