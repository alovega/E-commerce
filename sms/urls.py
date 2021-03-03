from django.conf.urls import url


from sms.views import incoming_delivery_reports, incoming_message

urlpatterns = [
	url(r'^delivery_report', incoming_delivery_reports, name= 'delivery_reports'),
	url(r'^incoming_message/$', incoming_message, name= 'incoming_messages'),
]
