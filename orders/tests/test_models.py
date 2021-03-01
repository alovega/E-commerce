"""
Tests for models in orders module
"""

import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestOrdersModels(object):
	"""
	Test class for core models
	"""
	def test_orders(self):
		order = mixer.blend("orders.Order")
		assert order is not None, "Should create an Order"
		assert type(str(order)) == str, "Order Should be a str object"

	def test_incident(self):
		item = mixer.blend("orders.Item")
		assert item is not None, "Should create an Item"
		assert type(str(item)) == str, "Item Should be a str object"
