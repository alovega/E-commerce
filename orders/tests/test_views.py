"""
This is the user views tests module.
"""
import ast

import pytest
from mixer.backend.django import mixer
from django import urls
from orders.models import Item, Order

pytestmark = pytest.mark.django_db


def test_item_creation(client, test_data, item_data):
	assert Item.objects.count() == 0
	creation_url = urls.reverse('create_item')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	response = client.post(creation_url, item_data, **headers)
	assert Item.objects.count() == 1
	assert response.status_code == 200


def test_item_creation_with_no_data(client, test_data, item_data = None):
	assert Item.objects.count() == 0
	creation_url = urls.reverse('create_item')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	response = client.post(creation_url, item_data, **headers)
	assert Item.objects.count() == 0
	assert response.status_code == 200


def test_order_creation(client, test_data):
	assert Order.objects.count() == 0
	creation_url = urls.reverse('create_order')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	item = mixer.blend('orders.Item', total = 400, price = 20)
	response = client.post(creation_url, {'item': item.id, 'quantity': 20}, **headers)
	assert Order.objects.count() == 1
	assert response.status_code == 200


def test_order_creation_with_no_data(client, test_data):
	assert Order.objects.count() == 0
	creation_url = urls.reverse('create_order')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	response = client.post(creation_url, None, **headers)
	assert Order.objects.count() == 0
	assert response.status_code == 200


def test_item_update(client, test_data):
	assert Item.objects.count() == 0
	update_url = urls.reverse('update_item')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	item = mixer.blend('orders.Item', total = 400, price = 20)
	response = client.post(update_url, {'item': item.id, 'name': 'some test'}, **headers)
	dict_str = response.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data = item.get('data')
	assert response.status_code == 200
	assert data.get('name') == 'some test', 'Should have updated the item name'


def test_order_update(client, test_data):
	assert Item.objects.count() == 0
	update_url = urls.reverse('update_order')
	create_url = urls.reverse('create_order')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	item = mixer.blend('orders.Item', total = 400, price = 20)
	response1=client.post(create_url, {'item': item.id, 'quantity': 20}, **headers)
	dict_str = response1.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data = item.get('data')
	response = client.post(update_url, {'order': data.get('id'), 'quantity': 50}, **headers)
	dict_str = response.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data = item.get('data')
	assert response.status_code == 200
	assert data.get('quantity') == 50, 'ensure that the order quantity has been updated'


def test_get_item(client, test_data):
	assert Item.objects.count() == 0
	get_url = urls.reverse('get_item')
	create_url = urls.reverse('create_item')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	response1=client.post(create_url, {
		'name': 'test 2', 'description': 'post test2  things', 'total': 800, 'price': 20
	}, **headers)
	dict_str = response1.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data1 = item.get('data')
	response = client.post(get_url, {'item': data1.get('id')}, **headers)
	dict_str = response.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data = item.get('data')
	assert response.status_code == 200
	assert data1.get('name') == data.get('name'), 'ensure that the correct item has been retrieved'


def test_get_order(client, test_data):
	assert Item.objects.count() == 0
	get_url = urls.reverse('get_order')
	create_url = urls.reverse('create_order')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	item = mixer.blend('orders.Item', total = 400, price = 20)
	response1=client.post(create_url, {'item': item.id, 'quantity': 20}, **headers)
	dict_str = response1.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data1 = item.get('data')
	response = client.post(get_url, {'order': data1.get('id')}, **headers)
	dict_str = response.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data = item.get('data')
	assert response.status_code == 200
	assert data1.get('amount') == data.get('amount'), 'ensure that the correct order has been retrieved'


def test_get_all_item(client, test_data):
	assert Item.objects.count() == 0
	get_url = urls.reverse('get_items')
	create_url = urls.reverse('create_item')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	client.post(create_url, {
		'name': 'test 2', 'description': 'post test2  things', 'total': 800, 'price': 20
	}, **headers)
	response = client.post(get_url, **headers)
	dict_str = response.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data = item.get('data')
	assert response.status_code == 200
	assert len(data) == 1, 'ensure that the all items have been retrieved'


def test_get_all_order(client, test_data):
	assert Item.objects.count() == 0
	get_url = urls.reverse('get_orders')
	create_url = urls.reverse('create_order')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	item = mixer.blend('orders.Item', total = 400, price = 20)
	client.post(create_url, {'item': item.id, 'quantity': 20}, **headers)
	response = client.post(get_url, **headers)
	dict_str = response.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data = item.get('data')
	assert response.status_code == 200
	assert len(data) == 1, 'ensure that all the orders have been retrieved'


def test_delete_order(client, test_data):
	assert Item.objects.count() == 0
	delete_url = urls.reverse('delete_order')
	create_url = urls.reverse('create_order')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	item = mixer.blend('orders.Item', total = 400, price = 20)
	response1 = client.post(create_url, {'item': item.id, 'quantity': 20}, **headers)
	dict_str = response1.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data1 = item.get('data')
	response = client.post(delete_url, {'order': data1.get('id')}, **headers)
	dict_str = response.content.decode("UTF-8")
	data = ast.literal_eval(dict_str)
	assert response.status_code == 200
	assert data.get('code') == '200', 'ensure that the selected order have been deleted'


def test_delete_item(client, test_data):
	assert Item.objects.count() == 0
	delete_url = urls.reverse('delete_item')
	create_url = urls.reverse('create_item')
	headers = {
		'HTTP_AUTHORIZATION': 'Bearer {}'.format(test_data.get('access_token'))
	}
	response1=client.post(create_url, {
		'name': 'test 2', 'description': 'post test2  things', 'total': 800, 'price': 20
	}, **headers)
	dict_str = response1.content.decode("UTF-8")
	item = ast.literal_eval(dict_str)
	data1 = item.get('data')
	response = client.post(delete_url, {'item': data1.get('id')}, **headers)
	dict_str = response.content.decode("UTF-8")
	data = ast.literal_eval(dict_str)
	assert response.status_code == 200
	assert data.get('code') == '200', 'ensure that the selected item have been deleted'
