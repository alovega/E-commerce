"""
Class for Item Administration
"""

import logging
from django.db.models import F

from orders.backend.services import ItemService

lgr = logging.getLogger(__name__)


class ItemAdministrator(object):
	"""
	Class for Systems Administration
	"""

	@staticmethod
	def create_item(name, description, total, deficit, price, **kwargs):
		"""
		Creates an Item .
		@param name: The name of the item you are creating
		@type name: str
		@param description: Description of the item you are creating
		@type description: str/None
		@param total: Number of Items present
		@type total: int/None
		@param price: The cost of the item
		@type price: int/None
		@param kwargs: Extra key-value arguments to pass for item creation
		@return: Response code dictionary to indicate if the item was created or not
		@rtype: dict 
		"""
		try:
			if not price and not total and not description and not name:
				return {
					'code': '400',
					'message': 'Please input all required parameters: name, description, price, total'
				}
			item = ItemService().create(
				price = price, total = total, description=description, name=name)
			if item:
				item = ItemService().filter(pk = item.id).values(
					'id', 'name', 'description', 'price', 'total').first()
				return {"code": "200", 'data': item}
		except Exception as ex:
			lgr.exception("Item creation exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def update_item(item, name = None, description = None, total= None, price = None, **kwargs):
		"""
		Updates an Item .
		@param item: The id of the item you are updating
		@type item: str
		@param name: The name of the item you are updating
		@type name: str
		@param description: Description of the item you are updating
		@type description: str/None
		@param total: Number of Items present
		@type total: int/None
		@param price: The cost of the item
		@type price: int/None
		@param kwargs: Extra key-value arguments to pass for item update
		@return: Response code dictionary to indicate if the item was updated or not
		@rtype: dict
		"""
		try:
			item = ItemService().get(pk = item)
			if not item:
				return {'code': '400', 'message': 'item does not exist'}

			name = name if name is not None else item.name
			description = description if description is not None else item.description
			total = total if total is not None else item.total
			price = price if price is not None else item.price
			updated_item = ItemService().update(
				pk = item.id, name = name, description = description, total = total, price = price)
			if updated_item:
				updated_item = ItemService().filter(pk = item.id).values(
					'id', 'name', 'price', 'total', 'description', 'deficit', 'date_created', 'date_modified').first()
				return {'code': '200', 'data': updated_item}
		except Exception as ex:
			lgr.exception("Item Update exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_item(item, **kwargs):
		"""
		Retrieves an order.
		@param item: Id of the item to be retrieved
		@type item: str | None
		@param kwargs: Extra key-value arguments to pass for item retrieval
		@return: Response code dictionary to indicate if the item was retrieved or not
		@rtype: dict
		"""
		try:
			if item:
				item = ItemService().filter(pk=item).values(
					'id', 'name', 'description', 'price','total', 'deficit', 'date_created', 'date_modified').first()
			if item is None:
				return {"code": "400", 'message': 'item requested does not exist'}
			return {'code': '200', 'data': item}
		except Exception as ex:
			lgr.exception("Get item exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_items(**kwargs):
		"""
		Retrieves all created Items.
		@param kwargs: Extra key-value arguments to pass during item retrieval
		@return: Response code dictionary to indicate if the orders were retrieved or not
		@rtype: dict
		"""
		try:
			items = list(ItemService().filter().values().first())
			if items is None:
				return {"code": "400", 'message':'error while trying to fetch all items'}
			return {'code': '200', 'data': items}
		except Exception as ex:
			lgr.exception("fetching all items exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def delete_item(item, **kwargs):
		"""
		Deletes an item.
		@param item: item to be deleted
		@type item: str
		@return: Response code dictionary to indicate if the item was deleted or not
		@rtype: dict
		"""
		try:
			item = ItemService().filter(pk = item).first()
			if item is None:
				return {"code": "800.400.002", 'message': "no existing item"}
			if item.delete():
				return {'code': '800.200.001', 'Message': 'item deleted successfully'}
		except Exception as ex:
			lgr.exception("Delete item exception %s" % ex)
		return {"code": "400"}
