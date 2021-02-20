from django.conf.urls import url

from . import views
from .views import create_item, create_order, delete_item, delete_order, get_item, get_items, get_order, get_orders, \
	update_item, \
	update_order

urlpatterns = [
	url(r'^get_item/$', get_item, name = 'get_item'),
	url(r'^get_order/$', get_order, name = 'get_order'),
	url(r'^get_items/$', get_items, name = 'get_items'),
	url(r'^get_orders/$', get_orders, name = 'get_orders'),
	url(r'^create_item/$', create_item, name= 'create_item'),
	url(r'^create_order/$', create_order, name= 'create_order'),
	url(r'^update_item/$', update_item, name= 'update_item'),
	url(r'^update_order/$', update_order, name= 'update_order'),
	url(r'^delete_order/$', delete_order, name= 'delete_order'),
	url(r'^delete_item/$', delete_item, name= 'delete_item'),
]
