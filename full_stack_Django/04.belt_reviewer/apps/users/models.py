# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re

EMAIL_REGX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGX = re.compile(r'^[A-Za-z]\w+$')

# Create user Manager class
class UserManager(models.Manager):
	# Handle the login form
	def validate_login(self, post_data):
		errors = {}
		# Check for emptiness of fields
		for field, value in post_data.iteritems():
			if len(value) < 1:
				errors[field] = "{} field is required!".format(field)
		# Check for the user with this email in db
		if len(self.filter(email=post_data["email"])) > 0: # returns [] or [{}]
			# Store the retrieved user from db
			user = self.filter(email=post_data["email"])[0]
			# Compare user's passwords
			if not "password" in errors and not bcrypt.checkpw(post_data["password"].encode(), user.password.encode()):
				errors["password"] = "Invalid email or password!"
		else:
			errors["password"] = "Invalid email or password!"
		return errors

	# Login user method
	def login_user(self, post_data):
		user = self.filter(email=post_data["email"])[0]
		return user


	# Validate the registration form
	def validate_register(self, post_data):
		# object for store error messages
		errors = {}
		# Check for emptiness of fields
		for field, value in post_data.iteritems():
			if len(value) < 1:
				errors[field] = "{} field is required!".format(field.replace('_', ' '))
			# Check for the name and alias field min length
			if field == "name" or field == "alias":
				if not field in errors and len(value) < 2 and not re.match(NAME_REGX, post_data[field]):
					errors[field] = "{} field must be at least 2 characters long and letters only!".format(field)
			# checking for valid email address
			if field == "email":
				if not field in errors and not re.match(EMAIL_REGX, post_data["email"]):
					errors[field] = "Invalid email address!"
			# Check for password length
			if field == "password":
				if not field in errors and len(value) < 8:
					errors[field] = "{} field must be at least 8 characters long!".format(field)
				if post_data[field] != post_data["confirm_password"]:
					errors[field] = "Passwords don't match!"
		# prevent the user from registering multiple times with the same email
		if len(self.filter(email=post_data["email"])) > 1: # this returns [] or [{}]
			errors["email"] = "Invalid email creditial!"
		return errors

	# register user
	def register_user(self, post_data):
		# If there are no errors, then create a new user and hash the password
		# Encrypt the password and insert into db
		pw_hash= bcrypt.hashpw((post_data["password"].encode()), bcrypt.gensalt(5))
		new_user = self.create(
			name=post_data["name"],
			alias=post_data["alias"],
			email=post_data["email"],
			password= pw_hash
		)
		return new_user


# Create your models here.
class User(models.Model):
	name = models.CharField(max_length=200)
	alias = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	objects = UserManager()


	# def __str__(self):
	# 	print "<User object: Name: {}, Alias: {}, Email: {}, Password: {}".format(self.name, self.alias, self.email, self.password)

