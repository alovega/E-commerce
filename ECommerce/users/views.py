from __future__ import unicode_literals

import logging

from django.http import JsonResponse

# Create your views here.
from django.views.decorators.csrf import csrf_exempt

from base.utility import get_request_data
from users.backend.interfaces.user_interface import UserAdministrator

lgr = logging.getLogger(__name__)


@csrf_exempt
def register_user(request, *args, **kwargs):
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
		item = UserAdministrator.create_user(
			username=data.get('username'), password = data.get('password'), email = data.get('email'),
			first_name = data.get('first_name'), last_name = data.get('last_name'), phone_number = data.get(
				'phone_number'))
		return JsonResponse(item)
	except Exception as ex:
		lgr.exception('User registration Exception: %s' % ex)
	return JsonResponse({'code': '500'})
