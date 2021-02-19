from ..models import Order, Item

from ECommerce.base.servicebase import ServiceBase


class ItemService(ServiceBase):
	"""
	Service for SystemService CRUD
	"""
	manager = Item.objects


class OrderService(ServiceBase):
	"""
	Service for Interface CRUD
	"""
	manager = Order.objects
