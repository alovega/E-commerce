"""
Class for Orders Administration
"""

import logging
from django.db.models import F

from orders.backend.services import OrderService, ItemService
from orders.backend.interfaces.item_interface import ItemAdministrator
from oidc_provider.models import Token

from users.models import CustomUser

lgr = logging.getLogger(__name__)


class OrderAdministrator(object):
	"""
	Class for Systems Administration
	"""

	@staticmethod
	def create_order(quantity, item, **kwargs):
		"""
		Creates an order.
		@param quantity: The quantity of the order you are making
		@type quantity: int
		@param item: The id of the item you are ordering
		@type item: str/None
		@param kwargs: Extra key-value arguments to pass for order creation
		@return: Response code dictionary to indicate if the order was created or not
		@rtype: dict
		"""
		try:
			item = ItemService().get(pk = item)
			# check if item exist
			if not item:
				return {'code': '400', 'message': 'Item does not exist'}
			# check if item is replenished
			if not item.total:
				return {'code': '503', 'message': 'this service is currently unavailable'}
			# ensure the ordered quantity does not exceed item total
			if item.total < int(quantity):
				return {
					'code': '406',
					'message': 'your order exceeds the available item please reduce your order or wait'
				}
			amount = int(quantity) * int(item.price)
			order = OrderService().create(
				quantity = quantity, amount = int(amount), item = item,
				customer = CustomUser.objects.get(id = kwargs.get('token').user_id))
			if order:
				# if creation successful update item total
				ItemAdministrator.update_item(item = item.id, total = (int(item.total) - int(quantity)))
				order = OrderService().filter(pk = order.id).values(
					'amount', 'id', 'quantity', 'date_created', 'date_modified',
					item_name = F('item__name'), owner = F('customer__username')).first()
				return {"code": "200", 'data': order}
		except Exception as ex:
			lgr.exception("Order creation exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def update_order(order, quantity = None, item = None, **kwargs):
		"""
		Updates a system.
		@param order: Id of the order
		@type order: str | None
		@param quantity: number of items you are ordering
		@type quantity: int | None
		@param item: id of the item you are ordering
		@type item: str | None
		@param kwargs: Extra key-value arguments to pass for order update
		@return: Response code dictionary to indicate if the order was updated or not
		@rtype: dict
		"""
		try:
			order = OrderService().get(pk = order)
			user = CustomUser.objects.get(pk = kwargs.get('token').user_id)
			# ensure order exist
			if not order:
				return {'code': '400', 'message': 'order does not exist'}
			# ensure updated order belongs to the authenticated user
			if user.id != order.customer.id:
				return {'code': '400', 'message': 'you are not authorized to update this order'}
			# ensure item exist
			if item is not None:
				item = ItemService().get(pk = item)
				if not item:
					return {'code': '400', 'message': 'Item does not exist'}
				# if it's a change in item prompt the customer to make a new order
				if item.id != order.item.id:
					return {'code': '400', 'message': 'Please make a new order this change is forbidden'}
			print(item)

			if quantity:
				# implement logic of updating item total
				print(item)
				if int(quantity) > order.quantity:
					update = ItemAdministrator.update_item(
						item = item.id,
						total = (int(item.total) - (int(quantity) - int(order.quantity)))
					)
					if not update:
						return {'code': '400', 'message': 'unable to update item'}
					quantity = quantity
				elif order.quantity > int(quantity):
					update = ItemAdministrator.update_item(
						item = item.id,
						total = (int(item.total) + (int(order.quantity) - int(quantity)))
					)
					if not update:
						return {'code': '400', 'message': 'unable to update item'}
					quantity = quantity
				else:
					quantity = order.quantity

			amount = quantity * ItemService().get(id = item).price if ItemService().get(id = item) is not None \
				else order.amount
			updated_order = OrderService().update(
				pk = order.id, quantity = quantity, amount = amount, item = item, customer = user)
			if updated_order:
				updated_order = OrderService().filter(pk = order.id).values(
					'id', 'quantity', 'amount', 'date_created', 'date_modified', item_name = F('item__name'),
					owner = F('customer__username')
				).first()
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
			if order:  # ensure a customer is only getting an order tied to him
				order = OrderService().filter(
					pk = order, customer = CustomUser.objects.get(pk = kwargs.get('token').user_id)).values(
					'id', 'quantity', 'amount', 'date_created', 'date_modified', item_name = F('item__name')
				).first()
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
			# ensure a customer is getting only orders tied to them
			orders = list(OrderService().filter(
				customer = CustomUser.objects.get(pk = kwargs.get('token').user_id)
			).values('id', 'quantity', 'amount', 'date_created', 'date_modified', item_name = F('item__name')))
			if orders is None:
				return {"code": "400", 'message': 'error while trying to fetch all orders'}
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
