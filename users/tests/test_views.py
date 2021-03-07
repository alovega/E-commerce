"""
This is the user views tests module.
"""

import pytest
from django import urls
from django.contrib.auth import get_user_model
from mixer.backend.django import mixer

# noinspection SpellCheckingInspection
from ..backend.services import CustomUserService

pytestmark = pytest.mark.django_db


@pytest.mark.parametrize('param', ['registration'])
def test_render_views(client, param):
	temp_url = urls.reverse(param)
	response = client.get(temp_url)
	assert response.status_code == 200


def test_user_registration(client, user_data):
	user_model = get_user_model()
	assert user_model.objects.count() == 0
	registration_url = urls.reverse('registration')
	response = client.post(registration_url, user_data)
	assert user_model.objects.count() == 1
	assert response.status_code == 200


def test_user_registration_with_no_data(client, data = None):
	if data is None:
		data = {}
	user_model = get_user_model()
	assert user_model.objects.count() == 0
	registration_url = urls.reverse('registration')
	client.post(registration_url, data)
	assert user_model.objects.count() == 0
