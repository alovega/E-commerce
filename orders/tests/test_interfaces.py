import pytest
from mixer.backend.django import mixer

from orders.backend.interfaces.order_interface import OrderAdministrator
from orders.backend.interfaces.item_interface import ItemAdministrator
from users.models import CustomUser

pytestmark = pytest.mark.django_db


class TestOrderInterface(object):
	pass


class TestItemInterface(object):
	pass
