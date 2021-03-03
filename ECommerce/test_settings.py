"""
The test settings for ECommerce.
"""

from .settings import *

# Database
# https://docs.djangoproject.com/en/1.10/ref/settings/#databases

DATABASES = {
	'default': {
		'ENGINE': 'django.db.backends.postgresql',
		'USER': config('DATABASE_USER'),
		'PASSWORD': config('DATABASE_PASSWORD'),
		'NAME': config('DATABASE_TEST')
	}
}
EMAIL_BACKEND = 'django.core.mail.backends.locmem.EmailBackend'
