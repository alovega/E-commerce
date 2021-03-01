"""
This is the orders services tests module.
"""
import pytest
from mixer.backend.django import mixer

# noinspection SpellCheckingInspection
from ..backend.services import OrderService, ItemService

pytestmark = pytest.mark.django_db


class TestOrderService(object):
	"""
	Test the System Model Services
	"""

	def test_get(self):
		"""
		Test System get service
		"""
		mixer.blend('orders.Order', quantity = 10)
		order = OrderService().filter()
		assert len(order) == 1, 'Should have an order object'

	def test_filter(self):
		"""
		Test System filter service
		"""
		mixer.cycle(3).blend('orders.Order')
		orders = OrderService().filter()
		assert len(orders) == 3, 'Should have 3 Order objects'

	def test_create(self):
		"""
		Test System create service
		"""
		item = mixer.blend('orders.Item')
		order = OrderService().create(quantity = 10, item = item)
		assert order is not None, 'Should have an order object'
		assert order.quantity == 10, 'Created an order with 10 as quantity'

	def test_update(self):
		"""
		Test System update service
		"""
		order = mixer.blend('orders.Order')
		order = OrderService().update(order.id, quantity = 200)
		assert order.quantity == 200, 'Should have updated quantity as 200'


class TestItemService(object):
	"""
	Test the System Model Services
	"""

	def test_get(self):
		"""
		Test System get service
		"""
		mixer.blend('orders.Item', name = "Mobile Tablet")
		item = ItemService().get(name = "Mobile Tablet")
		assert item.name == "Mobile Tablet", 'Should have an item with name Mobile Tablet'

	def test_filter(self):
		"""
		Test System filter service
		"""
		mixer.cycle(3).blend('orders.Item')
		items = ItemService().filter()
		assert len(items) == 3, 'Should have 3 Items objects'

	def test_create(self):
		"""
		Test System create service
		"""
		item = ItemService().create(total = 1000, name = "writing pads", description = "papers for writing", price = 60)
		assert item is not None, 'Should have an Item object'
		assert item.total == 1000, 'Created an item with 1000 as total'

	def test_update(self):
		"""
		Test System update service
		"""
		item = mixer.blend('orders.Item')
		new = ItemService().update(item.id, total = 200)
		assert new.total == 200, 'Should have updated item total as 200'
