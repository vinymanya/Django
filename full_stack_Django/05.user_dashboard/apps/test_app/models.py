# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
import bcrypt, re

# Create your models here.
EMAIL_REGX = re.compile(r'^[a-zA-Z0-9\.\+_-]+@[a-zA-Z0-9\._-]+\.[a-zA-Z]*$')
NAME_REGX = re.compile(r'^[A-Za-z]\w+$')
# Create your models here.
class UserManager(models.Manager):
	def validateLogin(self, post_data):
		#Do the validation logic here:
		#Filter method returns a list []
		errors = []
		#Check if the email exists in the db
		if len(self.filter(email=post_data["email"])) > 0:
			#check the user's password
			user = self.filter(email=post_data["email"])[0]
			if not bcrypt.checkpw(post_data["password"].encode(), user.password.encode()):
				errors.append("Invalid Email or Password!")
		else:
			errors.append("Invalid Email or Password!")
		if errors:
			return errors
		return user


	def validateRegister(self, post_data): # * will unpack a list and ** will unpack a dict
		errors = []
		#validate the names field based on length
		if len(post_data["first_name"]) < 2 or len(post_data["last_name"]) < 2:
			errors.append("Name fields must be at least 2 characters!")
		#validate the password's length
		if len(post_data["password"]) < 8:
			errors.append("password must be at least 8 characters!")
		#check name fields for letter characters
		if not re.match(NAME_REGX, post_data["first_name"]) or not re.match(NAME_REGX, post_data["last_name"]):
			errors.append("Name fields must be letter characters only!") 
		#Check for valid email
		if not re.match(EMAIL_REGX, post_data["email"]): # or if not EMAIL_REGX.match(post_data["email"]):
			errors.append("Invalid Email Address!")
		#check for uniqueness of email...prevent users from registering with multiple time with the same email
		if len(User.objects.filter(email= post_data["email"])) > 0:
			errors.append("Invalid email address!")
		#Compare password with confirm password
		if post_data["password"] != post_data["confirm_password"]:
			errors.append("Oops! passwords don't match!")
		if not errors:
			#Encrypt the password and insert into db
			pw_hash= bcrypt.hashpw((post_data["password"].encode()), bcrypt.gensalt(5))
			new_user = self.create(
				first_name=post_data["first_name"],
				last_name=post_data["last_name"],
				email=post_data["email"],
				password= pw_hash
			)
			return new_user
		return errors

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

			#preventing users from registering multiple times with the same email
		else:
			if len(self.filter(email=post_data["email"])) > 1:
				errors["email"] = "Invalid email cridential!"
		return errors

class User(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.EmailField(unique=True)
	password = models.CharField(max_length=255)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()

	def __str__(self):
		print "<First_name: {}, Last_name: {}, Email: {}, password: {}, Confirm_password: {}>".format(self.first_name, self.last_name, self.email, self.password, self.confirm_password)


class User2(models.Model):
	first_name = models.CharField(max_length=100)
	last_name = models.CharField(max_length=100)
	email = models.CharField(max_length=200)
	desc = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)
	objects = UserManager()
	
	def __repr__(self):
		return "First_name: {}, Last_name: {}, Email: {}".format(self.first_name, self.last_name, self.email)

# create a new classes and establish a relationship
class Message(models.Model):
	"""attributes for Message"""
	message = models.TextField(max_length=1000)
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)


class Comment(models.Model):
	"""attributes for Comment"""
	comment = models.TextField(max_length=1000)
	message = models.ForeignKey(Message, related_name = "comments")
	created_at = models.DateTimeField(auto_now_add=True)
	updated_at = models.DateTimeField(auto_now=True)

	


