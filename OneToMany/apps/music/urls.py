from django.conf.urls import url
from . import views

urlpatterns = [
	url(r'^$', views.index),
	url(r'^artists/create$', views.create_artist),
	url(r'^artists/(?P<artist_id>\d+)$', views.show_artist),
	url(r'^albums/create$', views.create_album),
	url(r'^albums/(?P<album_id>\d+)$', views.show_album)
]