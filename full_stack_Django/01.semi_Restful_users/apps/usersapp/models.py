# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import re


EMAIL_REGX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
# Create your models here.
class UserManager(models.Manager):
	def validate(self, post_data):
		print post_data
		errors = {}
		#Let's check whether or not all fields are empty
		for field, value in post_data.iteritems():
			if len(value) < 1:
				errors[field] = "{} field is required!".format(field.replace('_', ''))
			# check for name field min length
			if field == "first_name" or field == "last_name":
				if not field in errors and len(value) < 2:
					errors[field] = "{} field must be at least 2 characters".format(field.replace('_',''))
		#checking for valid email address
		if not "email" in errors and not re.match(EMAIL_REGX, post_data["email"]):
			errors["email"] = "Invalid email address!"

			#preventing users from registering multiple times with the same email.
		else:
			if len(self.filter(email=post_data["email"])) > 1: # this returns [] or [{}]
				errors["email"] = "Inlid email cridential!"
		return errors


class User(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=200)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	
	def __repr__(self):
		return "First_name: {}, Last_name: {}, Email: {}".format(self.first_name, self.last_name, self.email)

	


