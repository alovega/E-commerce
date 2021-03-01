from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _


class CustomUser(AbstractUser):
	"""
	Model for managing system users
	"""
	phone_number = models.CharField(max_length=15, null=True, blank=True)

	# deleted = models.BooleanField(default = False)

	class Meta:
		db_table = 'auth_user'
		ordering = ('username',)
		unique_together = ('username',)
