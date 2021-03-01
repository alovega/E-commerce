import logging

import requests

from ECommerce import settings
from ..models import DeliveryReport, Outbox, Inbox

from base.servicebase import ServiceBase
lgr = logging.getLogger(__name__)


class InboxService(ServiceBase):
	"""
	Service for SystemService CRUD
	"""
	manager = Inbox.objects


class OutboxService(ServiceBase):
	"""
	Service for Interface CRUD
	"""
	manager = Outbox.objects

	def send(self, **kwargs):
		"""
		This method creates an entry with the given kwargs as for the given manager.
		@param kwargs: key=>value methods to pass to the create method.
		@return: Created object or None on error.
		"""
		url = settings.AT_ENDPOINT_URL
		headers = {
			'ApiKey': settings.AT_API_KEY,
			'Content-Type': 'application/x-www-form-urlencoded',
			'Accept': 'application/json'
		}
		body = {
			'username': settings.AT_USER_NAME,
			'from': settings.AT_FROM_VALUE,
			'message': kwargs['message'],
			'to': kwargs['phone_number']
		}
		response = requests.post(url=url, headers=headers, data=body)
		print(response.__dict__)
		data = response.json().get('SMSMessageData').get('Recipients')[0]
		try:
			if 'pk' in kwargs and self.manager.get(pk = kwargs.get('pk', '')):
				return self.manager.get(pk = kwargs.get('pk', ''))  # Returned Object.
			if self.manager is not None:
				return self.manager.create(
					status=data['status'],
					statusCode=data['statusCode'],
					phone=data['number'],
					text=kwargs['message'],
					messageId=data['messageId']
				)
		# return self.manager.create(**kwargs)
		except Exception as e:
			lgr.exception('%sService create exception: %s' % (self.manager.model.__name__, e))
		return None
		# Outbox_object = Outbox(
		# )
		# Outbox_object.save()

	def create(self, **kwargs):
		"""
		This method creates an entry with the given kwargs as for the given manager.
		@param kwargs: key=>value methods to pass to the create method.
		@return: Created object or None on error.
		"""
		try:
			if 'pk' in kwargs and self.manager.get(pk = kwargs.get('pk', '')):
				return self.manager.get(pk = kwargs.get('pk', ''))  # Returned Object.
			if self.manager is not None:
				return self.send(**kwargs)
			# return self.manager.create(**kwargs)
		except Exception as e:
			lgr.exception('%sService create exception: %s' % (self.manager.model.__name__, e))
		return None


class DeliveryReportService(ServiceBase):
	"""
	Service for Interface CRUD
	"""
	manager = DeliveryReport.objects
