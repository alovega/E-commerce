"""
Class for Orders Administration
"""

import logging
from django.db.models import F

from sms.backend.services import DeliveryReportService

lgr = logging.getLogger(__name__)


class DeliveryReportAdministrator(object):
	"""
	Class for DeliveryReport Administration
	"""

	@staticmethod
	def create_delivery_report(phone_number, retry_count, identifier, status, network_code, **kwargs):
		"""
		Creates an outbox message.
		@param phone_number: The users phone_number
		@type phone_number: char
		@param retry_count: Number of times the request to send a message to the device was retried before it succeeded
		@type retry_count: str/None
		@param network_code: A unique identifier for the telco that handled the message.
		@type network_code: str/None
		@param identifier: A unique identifier for each message.
		@type identifier: str/None
		@param status: The status of the message
		@type status: str/None
		@param kwargs: Extra key-value arguments to pass for delivery report creation
		@return: Response code dictionary to indicate if the delivery report was created or not
		@rtype: dict
		"""
		try:
			report = DeliveryReportService().create(
				phone_number = phone_number, identifier = identifier, retry_count = retry_count,
				status = status, network_code= network_code, **kwargs)
			if report:
				delivery_report = DeliveryReportService().filter(pk = report.id).values(
					'id', 'status', 'retry_count', 'network_code', 'identifier', 'phone_number', 'date_created').first()
				return {"code": "200", 'data': delivery_report}
		except Exception as ex:
			lgr.exception("Delivery report creation exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_delivery_report(report, **kwargs):
		"""
		Retrieves an delivery report.
		@param report: Id of the delivery report to be retrieved
		@type report: str | None
		@param kwargs: Extra key-value arguments to pass for delivery report filtering
		@return: Response code dictionary to indicate if the delivery report was retrieved or not
		@rtype: dict
		"""
		try:
			if report:  # ensure a customer is only getting an order tied to him
				delivery_report = DeliveryReportService().filter(
					pk = report).values(
					'id', 'status', 'retry_count', 'network_code', 'identifier', 'phone_number', 'date_created').first()
			if delivery_report is None:
				return {"code": "400", 'message': 'delivery report requested does not exist'}
			return {'code': '200', 'data': delivery_report}
		except Exception as ex:
			lgr.exception("Get delivery report exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def get_all_delivery_reports(**kwargs):
		"""
		Retrieves all created Outbox messages.
		@param kwargs: Extra key-value arguments to pass for order filtering
		@return: Response code dictionary to indicate if the orders were retrieved or not
		@rtype: dict
		"""
		try:
			# ensure a customer is getting only orders tied to them
			reports = list(DeliveryReportService().filter().values(
				'id', 'status', 'retry_count', 'network_code', 'identifier', 'phone_number', 'date_created'))
			if reports is None:
				return {"code": "400", 'message': 'error while trying to fetch all delivery reports'}
			return {'code': '200', 'data': reports}
		except Exception as ex:
			lgr.exception("Get all delivery reports exception %s" % ex)
		return {"code": "400"}

	@staticmethod
	def delete_delivery_report(report, **kwargs):
		"""
		Deletes an outbox message.
		@param report: report  to be deleted
		@type report: str
		@return: Response code dictionary to indicate if the report was deleted or not
		@rtype: dict
		"""
		try:
			report = DeliveryReportService().filter(pk = report).first()
			if report is None:
				return {"code": "800.400.002"}
			if report.delete():
				return {'code': '800.200.001', 'Message': 'Delivery report deleted successfully'}
		except Exception as ex:
			lgr.exception("Delete delivery report message exception %s" % ex)
		return {"code": "400"}
