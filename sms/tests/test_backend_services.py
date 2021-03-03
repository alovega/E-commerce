"""
This is the sms services tests module.
"""
import datetime

import pytest
from mixer.backend.django import mixer

# noinspection SpellCheckingInspection
from ..backend.services import DeliveryReportService, OutboxService, InboxService

pytestmark = pytest.mark.django_db


class TestOutboxService(object):
	"""
	Test the Outbox Model Services
	"""

	def test_get(self):
		"""
		Test Outbox get service
		"""
		mixer.blend('sms.Outbox')
		outbox = OutboxService().filter()
		assert len(outbox) == 1, 'Should have an outbox object'

	def test_get_with_no_data(self):
		"""
		Test Outbox get service
		"""
		outbox = OutboxService().get()
		outbox2 = OutboxService().get(simple = 'data')
		assert outbox is None, 'Should have no object'
		assert outbox2 is None, 'Should have no object'

	def test_filter(self):
		"""
		Test outbox filter service
		"""
		mixer.cycle(3).blend('sms.Outbox')
		outboxes = OutboxService().filter()
		assert len(outboxes) == 3, 'Should have 3 Outbox objects'

	def test_filter_with_no_data(self):
		"""
		Test outbox filter service
		"""
		outboxes = OutboxService().filter(text='someone')
		outboxes2 = OutboxService().filter(simple='something')
		assert len(outboxes) == 0, 'Should have no Outbox objects'
		assert outboxes2 is None, 'Should have no Outbox objects'

	def test_create(self):
		"""
		Test Outbox create service
		"""
		outbox = OutboxService().create(message = 'simple test', phone_number = '+254748276871')
		assert outbox is not None, 'Should have an outbox object'
		assert outbox.text == 'simple test', 'Created an outbox with given message'

	def test_creation_outbox__failure(self):
		"""
		Test Outbox create service
		"""
		outbox = OutboxService().create(message = 12345669556, phone_number = 1234545666)
		print(outbox)
		assert outbox is None, 'Should have an exception'

	def test_creation_with__empty_parameters_(self):
		"""
		Test Outbox create service
		"""
		outbox = OutboxService().create()
		print(outbox)
		assert outbox is None, 'Should have an exception'

	def test_update(self):
		"""
		Test Outbox update service
		"""
		message = mixer.blend('sms.Outbox')
		outbox = OutboxService().update(message.id, message = 'simple test 2')
		assert outbox.message == 'simple test 2', 'Should have updated message as expected'


class TestInboxService(object):
	"""
	Test the Inbox Model Services
	"""

	def test_get(self):
		"""
		Test Inbox get service
		"""
		mixer.blend('sms.Inbox', text = "I have received it", phone = '+254723456575')
		inbox = InboxService().get(phone = '+254723456575')
		assert inbox.text == "I have received it", 'Should have an inbox with correct required name'

	def test_filter(self):
		"""
		Test Inbox filter service
		"""
		mixer.cycle(3).blend('sms.Inbox')
		inboxes = InboxService().filter()
		assert len(inboxes) == 3, 'Should have 3 Inbox objects'

	def test_create(self):
		"""
		Test Inbox create service
		"""
		inbox = InboxService().create(
			text = 'Simple sending message', phone = "+254717316934", to = '31644', linkId = '1234',
			date_created = datetime.datetime.now()
		)
		assert inbox is not None, 'Should have an Inbox object'
		assert inbox.text == 'Simple sending message', 'Created an inbox with required message'

	def test_inbox_creation_with_empty_data(self):
		"""
		Test Inbox create service
		"""
		inbox = InboxService().create()
		assert inbox is  None, 'Should have an Inbox object'

	def test_update(self):
		"""
		Test System update service
		"""
		inbox = mixer.blend('sms.Inbox')
		new = InboxService().update(inbox.id, message = 'someone')
		assert new.message == 'someone', 'Should have updated inbox message'

	def test_lock_for_update(self):
		"""
		Test System update service
		"""
		inbox = mixer.blend('sms.Inbox')
		new = InboxService(lock_for_update = True).update(inbox.id, message = 'someone')
		assert new.message == 'someone', 'Should have updated inbox message'

	def test_update_non_existant_field(self):
		"""
		Test System update service
		"""
		inbox = mixer.blend('sms.Inbox')
		new = InboxService().update(34, kevin = 'someone')
		sample = InboxService().update(inbox.id, phone=234552222784645444282882282882)
		assert  sample is None
		assert new is None, 'Should return None'


class TestDeliveryReportService(object):
	"""
	Test the delivery report Model Services
	"""

	def test_get(self):
		"""
		Test  delivery report get service
		"""
		mixer.blend('sms.DeliveryReport', identifier = "aa1234nrc234", phone_number = '+254723456575')
		report = DeliveryReportService().get(phone_number = '+254723456575')
		assert report.identifier == "aa1234nrc234", 'Should have a report  with correct identifier'

	def test_filter(self):
		"""
		Test delivery report filter service
		"""
		mixer.cycle(3).blend('sms.DeliveryReport')
		reports = DeliveryReportService().filter()
		assert len(reports) == 3, 'Should have 3 report objects'

	def test_create(self):
		"""
		Test Delivery report create service
		"""
		report = DeliveryReportService().create(
			identifier = 'aa1234nrc234', phone_number = "+254717316934", retry_count = 4, status = 'failed',
			network_code = 8
		)
		assert report is not None, 'Should have an Inbox object'
		assert report.identifier == 'aa1234nrc234', 'Created a report with correct identifier'

	def test_update(self):
		"""
		Test Delivery report update service
		"""
		report = mixer.blend('sms.DeliveryReport')
		new = DeliveryReportService().update(report.id, retry_count = 22)
		assert new.retry_count == 22, 'Should have updated report retry count'
