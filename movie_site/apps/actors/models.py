# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import datetime


# Create your manager here
class ActorManager(models.Manager):
	def validate_actor(self, post_data):
		errors = []
		if post_data.get("first_name") == "":
			errors.append("First Name cannot be empty!")
		if post_data.get("last_name") == "":
			errors.append("Last Name cannot be empty!")
		# Validate the date of birth
		try:
			dob = datetime.datetime.strptime(post_data["dob"], "%Y-%m-%d")
			today = datetime.datetime.today()
			if dob > today:
				errors.append("Date of Birth cannot be in the future!")
		# Flash an error msg when no dob is provided
		except:
			errors.append("Date of Birth field cannot be empty!!!")
		return errors


# Create your models here.
class Actor(models.Model):
	first_name = models.CharField(max_length=255)
	last_name = models.CharField(max_length=255)
	dob = models.DateField()
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = ActorManager()


