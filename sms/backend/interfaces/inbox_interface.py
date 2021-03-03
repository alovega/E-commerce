"""
Class for Orders Administration
"""

import logging
from django.db.models import F

from sms.backend.services import InboxService

lgr = logging.getLogger(__name__)


class InboxAdministrator(object):
	"""
	Class for inbox message Administration
	"""

	@staticmethod
	def create_inbox(date_created, text, phone, to, linkId,  **kwargs):
		"""
		Creates an inbox message.
		@param date_created: The date it was created
		@type date_created: str
		@param phone: The senders phone_number
		@type phone: char
		@param text: The text that was sent by the user
		@type text: str/None
		@param to: Your registered short code that the sms was sent out to
		@type to: int
		@param linkId: A unique identifier attached to each incoming message.
		@type linkId: char
		@param kwargs: Extra key-value arguments to pass for inbox creation
		@return: Response code dictionary to indicate if the inbox message was created or not
		@rtype: dict
		"""
		try:
			message = InboxService().create(
				phone = phone, text = text, date_created = date_created, to = to, linkId = linkId, **kwargs)
			if message:
				inbox = InboxService().filter(pk = message.id).values(
					'id', 'linkId', 'text', 'phone', 'date_created').first()
				return {"code": "200", 'data': inbox}
		except Exception as ex:
			lgr.exception("Inbox message creation exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_inbox(inbox, **kwargs):
		"""
		Retrieves an inbox message.
		@param inbox: Id of the inbox message to be retrieved
		@type inbox: str | None
		@param kwargs: Extra key-value arguments to pass for inbox filtering
		@return: Response code dictionary to indicate if the inbox was retrieved or not
		@rtype: dict
		"""
		try:
			if inbox:
				message = InboxService().filter(
					pk = inbox).values(
					'id', 'linkId', 'text', 'phone', 'date_created').first()
			if message is None:
				return {"code": "400", 'message': 'inbox requested does not exist'}
			return {'code': '200', 'data': message}
		except Exception as ex:
			lgr.exception("Get inbox exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_all_inbox(**kwargs):
		"""
		Retrieves all created inbox messages.
		@param kwargs: Extra key-value arguments to pass for inbox filtering
		@return: Response code dictionary to indicate if the inbox messages were retrieved or not
		@rtype: dict
		"""
		try:
			# ensure a customer is getting only orders tied to them
			messages = list(InboxService().filter().values(
				'id', 'linkId', 'text', 'phone', 'date_created'))
			if messages is None:
				return {"code": "400", 'message': 'error while trying to fetch all inbox messages'}
			return {'code': '200', 'data': messages}
		except Exception as ex:
			lgr.exception("Get all inbox message exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def delete_inbox(inbox, **kwargs):
		"""
		Deletes an inbox message.
		@param inbox: inbox message to be deleted
		@type inbox: str
		@return: Response code dictionary to indicate if the inbox was deleted or not
		@rtype: dict
		"""
		try:
			inbox = InboxService().filter(pk = inbox).first()
			if inbox is None:
				return {"code": "800.400.002"}
			if inbox.delete():
				return {'code': '800.200.001', 'Message': 'Inbox message deleted successfully'}
		except Exception as ex:
			lgr.exception("Delete inbox message exception %s" % ex)
		return {"code": "400"}
