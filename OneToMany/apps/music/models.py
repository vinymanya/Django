# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models

# Create your models here.

class Artist(models.Model):
	name = models.CharField(max_length=100)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name

class Album(models.Model):
	name = models.CharField(max_length=100)
	release_year = models.DateField()
	label = models.CharField(max_length=100)
	artist = models.ForeignKey(Artist, related_name="albums")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	def __str__(self):
		return self.name, self.label, self.release_year
	
