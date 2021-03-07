import ast

import pytest
from Cryptodome.PublicKey import RSA
from django import test, urls
from django.contrib.auth import get_user_model
from oidc_provider.models import Client, ResponseType, RSAKey


@pytest.fixture
def user_data():
	return {
		'email': 'test@example.com', 'username': 'test_user', 'password':'password', 'phone_number':'0789659291',
		'first_name': 'test', 'last_name': 'user'
	}


@pytest.fixture
def test_data(user_data):
	user_model = get_user_model()
	user_model.objects.create_user(**user_data)
	user_data['grant_type'] = 'password'
	key = RSA.generate(2048)
	r_key = RSAKey(key=key.exportKey('PEM').decode('utf8'))
	r_key.save()
	client = Client(
		name='Some Client', client_id='123', client_secret='456', redirect_uris=['http://example.com/'],
		scope=['openid']
	)
	client.save()
	client.response_types.add(ResponseType.objects.get(value='id_token token'))
	user_data['client_id'] = client.client_id
	user_data['scope'] = 'openid'
	user_data['client_secret'] = client.client_secret
	login_url = urls.reverse('oidc_provider:token')
	data = test.client.Client().post(path = login_url, data = user_data)
	dict_str = data.content.decode("UTF-8")
	my_data = ast.literal_eval(dict_str)
	return my_data


@pytest.fixture
def item_data():
	return {
		'name': 'something test', 'description': 'post testing things', 'total': 400, 'price': 20
	}


