from __future__ import unicode_literals

import logging

from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt
from oidc_provider.lib.utils.oauth2 import protected_resource_view

from base.utility import get_request_data
from orders.backend.interfaces.item_interface import ItemAdministrator
from orders.backend.interfaces.order_interface import OrderAdministrator

lgr = logging.getLogger(__name__)


@csrf_exempt
@protected_resource_view(['openid'])
def create_item(request, **kwargs):
	"""
	Creates item from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful item creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		item = ItemAdministrator.create_item(
			name = data.get('name'), description = data.get('description'), total = data.get('total'),
			price = data.get('price'))
		return JsonResponse(item)
	except Exception as ex:
		lgr.exception('Item creation Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@protected_resource_view(['openid'])
def create_order(request, **kwargs):
	"""
	Creates order from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful order creation or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		order = OrderAdministrator.create_order(
			quantity = data.get('quantity'), item = data.get('item'), **kwargs)
		return JsonResponse(order)
	except Exception as ex:
		lgr.exception('Order creation Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@protected_resource_view(['openid'])
def update_item(request, **kwargs):
	"""
	Updates item from users
	@param request: The Django WSGI Request to process
	@type request: WSGIRequest
	@return: A response code to indicate successful item update or otherwise
	@rtype: dict
	"""
	try:
		data = get_request_data(request)
		item = ItemAdministrator.update_item(
			item = data.get('item'), name = data.get('name'), description = data.get('description'),
			total = data.get('total'), price = data.get('price'), **kwargs)
		return JsonResponse(item)
	except Exception as ex:
		lgr.exception('Item update Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@protected_resource_view(['openid'])
def update_order(request, **kwargs):
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
			order= data.get('order'), quantity = data.get('quantity'), item = data.get('item'), **kwargs)
		return JsonResponse(order)
	except Exception as ex:
		lgr.exception('Order update Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@protected_resource_view(['openid'])
def get_order(request, **kwargs):
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
		order = OrderAdministrator.get_order(order = data.get('order'), **kwargs)
		return JsonResponse(order)
	except Exception as ex:
		lgr.exception('Order fetching Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@protected_resource_view(['openid'])
def get_item(request, **kwargs):
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
		item = ItemAdministrator.get_item(item = data.get('item'), **kwargs)
		return JsonResponse(item)
	except Exception as ex:
		lgr.exception('Item fetching Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@protected_resource_view(['openid'])
def get_items(request, **kwargs):
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
		items = ItemAdministrator.get_items(**kwargs)
		return JsonResponse(items)
	except Exception as ex:
		lgr.exception('Items fetching Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@protected_resource_view(['openid'])
def get_orders(request, **kwargs):
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
		orders = OrderAdministrator.get_orders(**kwargs)
		return JsonResponse(orders)
	except Exception as ex:
		lgr.exception('Orders fetching Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@protected_resource_view(['openid'])
def delete_order(request, **kwargs):
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
		order = OrderAdministrator.delete_order(order = data.get('order'), **kwargs)
		return JsonResponse(order)
	except Exception as ex:
		lgr.exception('Order deletion Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@protected_resource_view(['openid'])
def delete_item(request, **kwargs):
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
		item = ItemAdministrator.delete_item(item = data.get('item'), **kwargs)
		return JsonResponse(item)
	except Exception as ex:
		lgr.exception('Item deletion Exception: %s' % ex)
	return JsonResponse({'code': '500'})



