import pytest


@pytest.fixture
def user_data():
	return {
		'email': 'test@example.com', 'username': 'test_user', 'password':'password', 'phone_number':'0789659291',
		'first_name': 'test', 'last_name': 'user'
	}
