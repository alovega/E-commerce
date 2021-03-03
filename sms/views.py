import datetime

from django.http import JsonResponse
import logging
from django.utils.timezone import make_aware
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from sms.backend.interfaces.delivery_report_interface import DeliveryReportAdministrator
from sms.backend.interfaces.inbox_interface import InboxAdministrator

lgr = logging.getLogger(__name__)


@csrf_exempt
@require_POST
def incoming_message(request, **kwargs):
	"""
	sample incoming message from phone through AfricasTalking API
	{  'from': ['+2547278153xx'],
	 'linkId': ['28a92cdf-2d63-4ee3-93df-4233d3de0356'],
	   'text': ['heey this is a message from a phone'],
		 'id': ['b68d0989-d856-494f-92ee-7c439e96e1d9'],
	   'date': ['2021-01-14 08:10:15'],
		 'to': ['17163'] }
	"""
	try:
		date_created = request.POST.get('date')
		text = request.POST.get('text')
		phone = request.POST.get('from')
		to = request.POST.get('to')
		linkId = request.POST.get('linkId')
		date_created = datetime.datetime.strptime(date_created, '%Y-%m-%d %H:%M:%S')
		aware_datetime = make_aware(date_created)
		message = InboxAdministrator.create_inbox(
			phone = phone, text = text, to = to, linkId = linkId, date_created = aware_datetime, **kwargs)
		return JsonResponse(message)
	except Exception as ex:
		lgr.exception('Inbox message creation Exception: %s' % ex)
	return JsonResponse({'code': '500'})


@csrf_exempt
@require_POST
def incoming_delivery_reports(request, **kwargs):
	"""
	sample delivery report from Africas Talking API
	{'phoneNumber': ['+254727815xx'],
	  'retryCount': ['0'],
		  'status': ['Success'],
	 'networkCode': ['63902'],
			  'id': ['ATXid_29bc0ee2e3566472cd947d2f2918ab2f']}>
	"""
	try:
		print(request.POST.__dict__)
		phoneNumber = request.POST.get('phoneNumber')
		retryCount = request.POST.get('retryCount')
		status = request.POST.get('status')
		networkCode = request.POST.get('networkCode')
		identifier = request.POST.get('id')
		report = DeliveryReportAdministrator.create_delivery_report(
			phone_number = phoneNumber, retry_count = retryCount, status = status, network_code = networkCode,
			identifier = identifier, **kwargs)
		return JsonResponse(report)
	except Exception as ex:
		lgr.exception('Delivery report creation Exception: %s' % ex)
	return JsonResponse({'code': '500'})
