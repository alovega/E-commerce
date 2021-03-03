"""
Tests for models in orders model
"""

import pytest
from mixer.backend.django import mixer

pytestmark = pytest.mark.django_db


class TestUserModels(object):
	"""
	Test class for core models
	"""
	def test_custom_user(self):
		user = mixer.blend("users.CustomUser")
		assert user is not None, "Should create a user object"
		assert type(str(user)) == str, "User Should be a str object"
