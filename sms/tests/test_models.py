"""
Tests for models in sms model
"""

import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestSmsModels(object):
	"""
	Test class for core models
	"""
	def test_delivery_report(self):
		report = mixer.blend("sms.DeliveryReport")
		assert report is not None, "Should create a delivery Report"
		assert type(str(report)) == str, "report Should be a str object"

	def test_inbox(self):
		inbox = mixer.blend("sms.Inbox")
		assert inbox is not None, "Should create an Inbox message"
		assert type(str(inbox)) == str, "Inbox Should be a str object"

	def test_outbox(self):
		outbox = mixer.blend("sms.Outbox")
		assert outbox is not None, "Should create an outbox message"
		assert type(str(outbox)) == str, "Outbox Should be a str object"
