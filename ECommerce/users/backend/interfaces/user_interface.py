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
from oidc_provider.models import Client, ResponseType

lgr = logging.getLogger(__name__)


class UserAdministrator(object):
	"""
	Class for User Administration
	"""

	@staticmethod
	def create_user(username, password, email, first_name=None, last_name=None, phone_number=None, **kwargs):
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
			if CustomUser.objects.filter(username = username).exists():
				return {"code": "400", 'message': 'Username already in use'}
			if CustomUser.objects.filter(email = email).exists():
				return {"code": "400", 'message': 'Email already in use'}
			CustomUser.objects.create_user(
				username, email, password, first_name = first_name, last_name = last_name, phone_number = phone_number)
			return {"code": "200", 'message': 'user successfully registered'}
		except Exception as ex:
			lgr.exception("UserCreation exception %s" % ex)
		return {"code": "400", 'message': 'User could not be created'}
