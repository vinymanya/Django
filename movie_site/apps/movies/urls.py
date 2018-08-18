from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^title$', views.movies),
	url(r'^create_movie$', views.create_movie),
	url(r'^(?P<movie_id>\d+)/delete$', views.delete_movie)
]