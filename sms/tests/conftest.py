import pytest


@pytest.fixture
def incoming_report_data():
	return {
		'phoneNumber': ['+254727815xx'],
		'retryCount': ['0'],
		'status': ['Success'],
		'networkCode': ['63902'],
		'id': ['ATXid_29bc0ee2e3566472cd947d2f2918ab2f']
	}


@pytest.fixture
def incoming_message_data():
	return {
		'from': '+2547278153xx',
		'linkId': '28a92cdf-2d63-4ee3-93df-4233d3de0356',
		'text': 'heey this is a message from a phone',
		'id': 'b68d0989-d856-494f-92ee-7c439e96e1d9',
		'date': '2021-01-14 08:10:15',
		'to': '17163'
	}
