"""
Class for Orders Administration
"""

import logging
from django.db.models import F

from sms.backend.services import OutboxService

lgr = logging.getLogger(__name__)


class OutboxAdministrator(object):
	"""
	Class for outbox Administration
	"""

	@staticmethod
	def create_outbox(phone_number, message, **kwargs):
		"""
		Creates an outbox message.
		@param phone_number: The users phone_number
		@type phone_number: char
		@param message: The message that is going to be sent to the user
		@type message: str/None
		@param kwargs: Extra key-value arguments to pass for outbox message creation
		@return: Response code dictionary to indicate if the outbox message was created or not
		@rtype: dict
		"""
		try:
			message = OutboxService().create(
				phone_number = phone_number, message = message, **kwargs)
			if message:
				outbox = OutboxService().filter(pk = message.id).values(
					'id', 'status', 'statusCode', 'text', 'phone', 'date_created').first()
				return {"code": "200", 'data': outbox}
		except Exception as ex:
			lgr.exception("Message creation exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_outbox(outbox, **kwargs):
		"""
		Retrieves an outbox message.
		@param outbox: Id of the outbox message to be retrieved
		@type outbox: str | None
		@param kwargs: Extra key-value arguments to pass for outbox message filtering
		@return: Response code dictionary to indicate if the outbox message was retrieved or not
		@rtype: dict
		"""
		try:
			if outbox:
				message = OutboxService().filter(
					pk = outbox).values(
					'id', 'status', 'statusCode', 'text', 'phone', 'date_created').first()
			if message is None:
				return {"code": "400", 'message': 'outbox requested does not exist'}
			return {'code': '200', 'data': message}
		except Exception as ex:
			lgr.exception("Get outbox exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_all_outbox(**kwargs):
		"""
		Retrieves all created Outbox messages.
		@param kwargs: Extra key-value arguments to pass for outbox message filtering
		@return: Response code dictionary to indicate if the outbox message were retrieved or not
		@rtype: dict
		"""
		try:
			messages = list(OutboxService().filter().values(
				'id', 'status', 'statusCode', 'text', 'phone', 'date_created'))
			if messages is None:
				return {"code": "400", 'message': 'error while trying to fetch all outbox messages'}
			return {'code': '200', 'data': messages}
		except Exception as ex:
			lgr.exception("Get all outbox message exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def delete_outbox(outbox, **kwargs):
		"""
		Deletes an outbox message.
		@param outbox: outbox message to be deleted
		@type outbox: str
		@return: Response code dictionary to indicate if the outbox message was deleted or not
		@rtype: dict
		"""
		try:
			outbox = OutboxService().filter(pk = outbox).first()
			if outbox is None:
				return {"code": "800.400.002"}
			if outbox.delete():
				return {'code': '800.200.001', 'Message': 'Outbox message deleted successfully'}
		except Exception as ex:
			lgr.exception("Delete outbox message exception %s" % ex)
		return {"code": "400"}
