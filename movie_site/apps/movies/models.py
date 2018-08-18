# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from ..actors.models import Actor


# Create MovieManager
# Validate 'Movie' object from the form
class MovieManager(models.Manager):
	def validate_movie(self, post_data):
		errors = []
		if post_data["title"] == "":
			errors.append("Please, provide a title for the movie!")
		return errors


# Create your models here.
# Movie class
class Movie(models.Model):
	title = models.CharField(max_length=255)
	# Many to Many table between 'Actor' and 'Movie'
	# Connector table.
	actors = models.ManyToManyField(Actor, related_name="movies")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = MovieManager()
