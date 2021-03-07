import ast

import pytest
from mixer.backend.django import mixer
from django import urls
pytestmark = pytest.mark.django_db

from sms.models import DeliveryReport, Inbox


def test_create_incoming_delivery_reports(client, incoming_report_data):
	assert DeliveryReport.objects.count() == 0
	delivery_url = urls.reverse('delivery_reports')
	response = client.post(delivery_url, incoming_report_data)
	dict_str = response.content.decode("UTF-8")
	data = ast.literal_eval(dict_str)
	assert response.status_code == 200
	assert data.get('code') == '200', 'ensure that the selected item have been deleted'


def test_create_incoming_message_report(client, incoming_message_data):
	assert Inbox.objects.count() == 0
	message_url = urls.reverse('incoming_messages')
	response=client.post(message_url, incoming_message_data)
	dict_str = response.content.decode("UTF-8")
	data = ast.literal_eval(dict_str)
	assert response.status_code == 200
	assert data.get('code') == '200', 'ensure that the selected item have been deleted'
