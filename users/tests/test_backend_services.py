"""
This is the user services tests module.
"""

import pytest
from mixer.backend.django import mixer

# noinspection SpellCheckingInspection
from ..backend.services import CustomUserService

pytestmark = pytest.mark.django_db


class TestCustomUserService(object):
	"""
	Test the  custom user Model Services
	"""

	def test_get(self):
		"""
		Test   custom user get service
		"""
		mixer.blend('users.CustomUser', username = "kevin", phone_number = '+254723456575')
		user = CustomUserService().get(phone_number = '+254723456575')
		assert user.username == "kevin", 'Should have a user  with correct username'

	def test_filter(self):
		"""
		Test custom user filter service
		"""
		mixer.cycle(3).blend('users.CustomUser')
		users = CustomUserService().filter()
		assert len(users) == 3, 'Should have 3 user objects'

	def test_create(self):
		"""
		Test Custom User create service
		"""
		user = CustomUserService().create(
			username = 'kevin', phone_number = "+254717316934", email = 'sample@example.com', password = 'pass1234',
			first_name = 'kevin', last_name = 'someone'
		)
		assert user is not None, 'Should have created a user object'
		assert user.username == 'kevin', 'Created a user with correct username'

	def test_create_with_empty_parameters(self):
		"""
		Test Custom User create service
		"""
		kwargs = {'pk':'sem'}
		user = CustomUserService().create(username = '', email = '', password = '', **kwargs)
		assert user is  None, 'Should have created a user object'

	def test_update(self):
		"""
		Test custom user update service
		"""
		user = mixer.blend('users.CustomUser')
		new = CustomUserService().update(user.id, username = 'kelly')
		assert new.username == 'kelly', 'Should have updated username'
