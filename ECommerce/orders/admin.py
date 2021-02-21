from __future__ import unicode_literals

from django.contrib import admin
from orders.models import Item, Order


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
	"""
	Admin for custom user model
	"""
	list_filter = ('date_created', 'date_modified')
	list_display = ('id', 'quantity', 'amount', 'item', 'date_created', 'date_modified')
	ordering = ('-date_created',)
	search_fields = ('item__name',)


@admin.register(Item)
class ItemAdmin(admin.ModelAdmin):
	"""
	Admin for custom user model
	"""
	list_filter = ('date_created', 'date_modified')
	list_display = ('id', 'name', 'total', 'deficit', 'price', 'date_created', 'date_modified')
	ordering = ('-date_created',)
	search_fields = ('name', 'price')
