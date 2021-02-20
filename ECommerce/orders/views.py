from __future__ import unicode_literals

import logging
import calendar

from django.utils import timezone
from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from ECommerce.base.utility import get_request_data
from .interfaces.item_interface import ItemAdministrator
from .interfaces.order_interface import OrderAdministrator

lgr = logging.getLogger(__name__)


@csrf_exempt
def create_item(request):
	"""
	Creates item from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful item creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		item = ItemAdministrator.create_item(
			name = data.get('name'), description = data.get('description'), total = data.get('total'),
			price = data.get('price'))
		return JsonResponse(item)
	except Exception as ex:
		lgr.exception('Item creation Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
def create_order(request):
	"""
	Creates order from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful order creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		order = OrderAdministrator.create_order(
			quantity = data.get('quantity'), item_id = data.get('item_id'))
		return JsonResponse(order)
	except Exception as ex:
		lgr.exception('Order creation Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
def update_item(request):
	"""
	Updates item from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful item update or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		item = ItemAdministrator.update_item(
			item = data.get('item'), name = data.get('name'), description = data.get('description'),
			total = data.get('total'), price = data.get('price'))
		return JsonResponse(item)
	except Exception as ex:
		lgr.exception('Item update Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
def update_order(request):
	"""
	Updates order from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful order update or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		order = OrderAdministrator.update_order(
			order= data.get('order'), quantity = data.get('quantity'), item_id = data.get('item_id'))
		return JsonResponse(order)
	except Exception as ex:
		lgr.exception('Order update Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
def get_order(request):
	"""
	Retrieves order requested from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful order retrieval or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		order = OrderAdministrator.get_order(order = data.get('order'))
		return JsonResponse(order)
	except Exception as ex:
		lgr.exception('Order fetching Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
def get_item(request):
	"""
	retrieves item requested by users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful item retrieval or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		item = ItemAdministrator.get_item(item = data.get('item'))
		return JsonResponse(item)
	except Exception as ex:
		lgr.exception('Item fetching Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
def get_items(request):
	"""
	retrieves all item requested by users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful item retrieval or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		items = ItemAdministrator.get_items()
		return JsonResponse(items)
	except Exception as ex:
		lgr.exception('Items fetching Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
def get_orders(request):
	"""
	Retrieves all orders requested from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful order retrieval or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		orders = OrderAdministrator.get_orders()
		return JsonResponse(orders)
	except Exception as ex:
		lgr.exception('Orders fetching Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
def delete_order(request):
	"""
	delete an  order requested by users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful order deletion or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		order = OrderAdministrator.delete_order(item = data.get('order'))
		return JsonResponse(order)
	except Exception as ex:
		lgr.exception('Order deletion Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
def delete_item(request):
	"""
	delete item requested by users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful item deletion or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		print(data)
		item = ItemAdministrator.delete_item(item = data.get('item'))
		return JsonResponse(item)
	except Exception as ex:
		lgr.exception('Item deletion Exception: %s' % ex)
	return JsonResponse({'code': '500'})



