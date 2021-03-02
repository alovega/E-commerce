# coding=utf-8
"""
Class for User Administration
"""
import calendar
from datetime import timedelta
from django.utils import timezone
from django.db import IntegrityError

import logging
import dateutil.parser
from users.models import CustomUser
from django.db.models import F, Q
from users.backend.services import CustomUserService

lgr = logging.getLogger(__name__)


class UserAdministrator(object):
	"""
	Class for User Administration
	"""

	@staticmethod
	def create_user(username, password, email, first_name = None, last_name = None, phone_number = None, **kwargs):
		"""
		Creates a user.
		@param username: Username of the user to be created
		@type username: str
		@param email: Email of the user to be created
		@type email: str
		@param password: Password of the user to be created
		@type password: str
		@param first_name: First name of the user
		@type first_name: str | None
		@param last_name: Last name of the user
		@type last_name: str | None
		@param phone_number: Phone number of the user to be created
		@type email: str | None
		@param kwargs: Extra key-value arguments to pass for user creation
		@return: Response code dictionary to indicate if the user was created or not
		@rtype: dict
		"""
		try:
			if CustomUserService().filter(username = username).exists():
				return {"code": "400", 'message': 'Username already in use'}
			if CustomUserService().filter(email = email).exists():
				return {"code": "400", 'message': 'Email already in use'}
			if phone_number:  # ensure the user has given the required phone number
				a = len(phone_number) - 9
				new_mobile = phone_number[-1:a - 1:-1][::-1]
				if "+254" != phone_number.split(new_mobile)[0]:
					print(phone_number.split(new_mobile)[0])
					if len(phone_number.split(new_mobile)[0]) == 1:
						mobile_number = '+254' + new_mobile
					else:
						return 'Wrong phone number given'
				else:
					mobile_number = phone_number
			CustomUserService().create(
				username, email, password, first_name = first_name, last_name = last_name, phone_number = mobile_number)
			return {"code": "200", 'message': 'user successfully registered'}
		except Exception as ex:
			lgr.exception("UserCreation exception %s" % ex)
		return {"code": "400", 'message': 'User could not be created'}

	@staticmethod
	def get_user(user, **kwargs):
		"""
		Retrieves an order.
		@param order: Id of the order to be retrieved
		@type order: str | None
		@param kwargs: Extra key-value arguments to pass for order filtering
		@return: Response code dictionary to indicate if the order was retrieved or not
		@rtype: dict
		"""
		try:
			if user:  # fetch a user whom is a customer
				customer = CustomUserService().filter(
					pk = user).values().first()
			if customer is None:
				return {"code": "400", 'message': 'user requested does not exist'}
			return {'code': '200', 'data': user}
		except Exception as ex:
			lgr.exception("Get user exception %s" % ex)
		return {"code": "400"}


