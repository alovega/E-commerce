from django.db import models


# Create your models here.
from ECommerce import settings
from users.models import CustomUser


class Item(models.Model):
	name = models.CharField(max_length=100, null = True, help_text = "Name of the Item")
	description = models.CharField(max_length=1000, null = True, help_text = "Description of the Item")
	total = models.IntegerField(null = True, help_text = "Total amount of the item available")
	price = models.IntegerField(null = True,help_text = "Price of the Item")
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now = True)

	def __str__(self):
		return "%s" % self.name


class Order(models.Model):
	quantity = models.IntegerField(null=True, help_text="Please input only numbers character type.")
	customer = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete = models.CASCADE, blank = True, null = True)
	amount = models.IntegerField(null=True, help_text="Please input only numbers character type.")
	date_created = models.DateTimeField(auto_now_add=True)
	date_modified = models.DateTimeField(auto_now = True)
	item = models.ForeignKey(Item, on_delete =models.CASCADE)

	def __str__(self):
		return "%s" % self.item
