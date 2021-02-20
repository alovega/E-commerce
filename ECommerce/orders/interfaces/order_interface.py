"""
Class for Orders Administration
"""

import logging
from django.db.models import F

from orders.backend.services import OrderService, ItemService

lgr = logging.getLogger(__name__)


class OrderAdministrator(object):
	"""
	Class for Systems Administration
	"""

	@staticmethod
	def create_order(quantity, item_id, **kwargs):
		"""
		Creates an order.
		@param quantity: The quantity of the order you are making
		@type quantity: int
		@param item_id: The id of the item you are ordering
		@type item_id: str/None
		@param kwargs: Extra key-value arguments to pass for order creation
		@return: Response code dictionary to indicate if the order was created or not
		@rtype: dict
		"""
		try:
			item = ItemService().get(id = item_id)
			if not item:
				return {'code': '400', 'message': 'Item does not exist'}
			amount = quantity * item.price
			order = OrderService().create(
				quantity = quantity, amount = amount, item = item)
			if order:
				order = OrderService().filter(pk = order.id).values(
					'amount', 'id', 'quantity', 'date_created', 'date_modified',
					item_name = F('item__name')).first()
				return {"code": "200", 'data': order}
		except Exception as ex:
			lgr.exception("Order creation exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def update_order(order, quantity = None, item_id = None, **kwargs):
		"""
		Updates a system.
		@param order: Id of the order
		@type order: str | None
		@param quantity: number of items you are ordering
		@type quantity: int | None
		@param item_id: id of the item you are ordering
		@type item_id: str | None
		@param kwargs: Extra key-value arguments to pass for order update
		@return: Response code dictionary to indicate if the order was updated or not
		@rtype: dict
		"""
		try:
			order = OrderService().get(pk = order)
			if not order:
				return {'code': '400', 'message': 'order does not exist'}

			if item_id is not None:
				item = ItemService().get(id = item_id)
				if not item:
					return {'code': '400', 'message': 'Item does not exist'}

			quantity = quantity if quantity is not None else order.quantity
			amount = quantity * ItemService().get(id = item_id).price if ItemService().get(id = item_id) is not None \
				else order.amount
			item = ItemService().get(id = item_id) if item_id is not None else order.item
			updated_order = OrderService().update(
				pk = order.id, quantity = quantity, amount = amount, item = item)
			if updated_order:
				updated_order = OrderService().filter(pk = order.id).values(
					'id', 'quantity', 'amount', 'date_created', 'date_modified', item = F('item__name')).first()
				return {'code': '200', 'data': updated_order}
		except Exception as ex:
			lgr.exception("Order Update exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_order(order, **kwargs):
		"""
		Retrieves an order.
		@param order: Id of the order to be retrieved
		@type order: str | None
		@param kwargs: Extra key-value arguments to pass for order filtering
		@return: Response code dictionary to indicate if the order was retrieved or not
		@rtype: dict
		"""
		try:
			if order:
				order = OrderService().filter(pk=order).values(
					'id', 'quantity', 'amount', 'date_created', 'date_modified', item = F('item__name')).first()
			if order is None:
				return {"code": "400", 'message': 'order requested does not exist'}
			return {'code': '200', 'data': order}
		except Exception as ex:
			lgr.exception("Get order exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_orders(**kwargs):
		"""
		Retrieves all created Orders.
		@param kwargs: Extra key-value arguments to pass for order filtering
		@return: Response code dictionary to indicate if the orders were retrieved or not
		@rtype: dict
		"""
		try:
			orders = list(OrderService().filter().values(
				'id', 'quantity', 'amount', 'date_created', 'date_modified', item = F('item__name')).first())
			if orders is None:
				return {"code": "400", 'message':'error while trying to fetch all orders'}
			return {'code': '200', 'data': orders}
		except Exception as ex:
			lgr.exception("Get orders exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def delete_order(order, **kwargs):
		"""
		Deletes an order.
		@param order: order to be deleted
		@type order: str
		@return: Response code dictionary to indicate if the order was deleted or not
		@rtype: dict
		"""
		try:
			order = OrderService().filter(pk = order).first()
			if order is None:
				return {"code": "800.400.002"}
			if order.delete():
				return {'code': '800.200.001', 'Message': 'Order deleted successfully'}
		except Exception as ex:
			lgr.exception("Delete order exception %s" % ex)
		return {"code": "400"}
