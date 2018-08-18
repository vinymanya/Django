from django.conf.urls import url
from . import views


urlpatterns = [
	url(r'^$', views.dashboard),
	url(r'^add$', views.add),
	url(r'^create$', views.create),
	url(r'^(?P<book_id>\d+)$', views.book_detail),
	url(r'^(?P<book_id>\d+)/delete/(?P<review_id>\d+)$', views.delete_review),
	url(r'^(?P<book_id>\d+)/add_review/(?P<user_id>\d+)$', views.add_review)
]