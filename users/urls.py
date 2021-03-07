from django.conf.urls import url
from django.urls import include

from users.views import register_user

urlpatterns = [
	url(r'^register/$', register_user, name= 'registration'),
]
