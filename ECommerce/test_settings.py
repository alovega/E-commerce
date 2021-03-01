"""
The test settings for Helamonitor.
"""
import os

from .settings import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'USER': 'postgres',
		'PASSWORD':'LUG4Z1V4',
		'NAME': 'test_e_commerce',
	}
}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
