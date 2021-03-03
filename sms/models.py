import requests

from django.db import models
from django.conf import settings


# Create your models here.

class Outbox(models.Model):
	"""
	this model holds the messages that are generated and sent to the user
	"""
	status = models.CharField(max_length=10, blank=True, null=True)
	statusCode = models.IntegerField()
	phone = models.CharField(max_length=15)
	text = models.CharField(max_length=255)
	messageId = models.CharField(max_length=100)
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now = True)

	class Meta:
		ordering = ('-date_created',)
		verbose_name = "Outbox"
		verbose_name_plural = "Outbox"

	def __str__(self):
		return '{0}-{1}-{2}'.format(self.messageId, self.status, self.text[:10])  # noqa: E501


class DeliveryReport(models.Model):
	identifier = models.CharField(max_length=100)
	phone_number = models.CharField(max_length=15)
	retry_count = models.IntegerField()
	status = models.CharField(max_length=10, blank=True, null=True)
	network_code = models.IntegerField()
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now = True)

	class Meta:
		ordering = ('-date_created',)
		verbose_name = "Delivery Report"
		verbose_name_plural = "Delivery Reports"

	def __str__(self):
		return '{0}-{1}-{2}'.format(self.identifier, self.phone_number, self.status)  # noqa: E501


class Inbox(models.Model):
	"""This are message sent to the app from the user"""
	text = models.CharField(max_length=255)
	phone = models.CharField(max_length=15)
	to = models.IntegerField()
	linkId = models.CharField(max_length=100)
	date_created = models.DateTimeField(null=True, blank=True)
	date_modified = models.DateTimeField(auto_now = True)

	class Meta:
		ordering = ('-date_created',)
		verbose_name = "Inbox"
		verbose_name_plural = "Inbox"

	def __str__(self):
		return '{0}-{1}-{2}'.format(self.linkId, self.phone, self.text[:10])  # noqa: E501
