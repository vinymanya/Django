from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.index),
	url(r'^create$', views.create),
	url(r'^(?P<actor_id>\d+)$', views.show_actor),
	url(r'^(?P<actor_id>\d+)/delete$', views.delete_actor),
	url(r'^add_to_movie/(?P<actor_id>\d+)$', views.add_to_movie),
	url(r'^actors/(?P<actor_id>\d+)/remove_from_movie/(?P<movie_id>\d+)', views.remove_from_movie)
]