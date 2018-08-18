from django.conf.urls import url
from . import views

urlpatterns=[
	url(r'^$', views.index),
	url(r'^signin$', views.signin),
	url(r'^login$', views.login),
	url(r'^register$', views.register),
	url(r'^dashboard$', views.dashboard),
	url(r'^logout$', views.logout),
	url(r'^users/new$', views.new_user),
	url(r'^users/create$', views.create),
	url(r'^messages/(?P<id>\d+)$', views.messages),
	url(r'^comments/(?P<id>\d+)$', views.comments),
	url(r'^users/(?P<id>\d+)$', views.show),
	url(r'^users/(?P<id>\d+)/edit$', views.edit_user),
	url(r'^users/(?P<id>\d+)/update$', views.update),
	url(r'^users/(?P<id>\d+)/confirm$', views.confirm),
	url(r'^users/(?P<id>\d+)/delete$',  views.delete)
]