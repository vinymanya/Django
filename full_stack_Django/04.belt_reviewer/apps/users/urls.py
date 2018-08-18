from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.index),
	url(r'^login_form$', views.login_form),
	url(r'^register$', views.register),
	url(r'^login$', views.login),
	url(r'^(?P<user_id>\d+)$', views.show_user),
	url(r'^logout$', views.logout)
]