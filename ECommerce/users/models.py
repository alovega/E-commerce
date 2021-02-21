from django.db import models
from django.contrib.auth.models import AbstractUser
from django.utils.translation import ugettext_lazy as _

from .manager import CustomUserManager


class CustomUser(AbstractUser):
	phone_number = models.CharField(max_length=100, null = True, help_text = "Mobile/phone number of the user")
	code = models.CharField(max_length=100, null = True, help_text = "code of the user")

	objects = CustomUserManager()

	def __str__(self):
		return self.email
