# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import User
from ..books.models import Book, Review


# Create your views here.
def index(request):
	return render(request, "users/index.html")

# login form method
def login_form(request):
	return render(request, "users/login.html")

# register method
def register(request):
	if request.method == "POST":
		errors = User.objects.validate_register(request.POST)
		if len(errors):
			for field, error_msg in errors.iteritems():
				messages.error(request, error_msg, extra_tags=field)
			return redirect("/users")
		# Store the new_user that was created
		new_user = User.objects.register_user(request.POST)
		# Save user in session
		request.session["user_id"] = new_user.id
		messages.success(request, "You have successfully registered!, please Login")
		return redirect("/users/login_form")
	return redirect("/users")

# login method
def login(request):
	if request.method == "POST":
		errors = User.objects.validate_login(request.POST)
		if len(errors):
			for field, error_msg in errors.iteritems():
				messages.error(request, error_msg, extra_tags=field)
			return redirect("/users/login_form")
		# store the retuned user
		result = User.objects.login_user(request.POST)
		# Save user in session
		request.session["user_id"] = result.id
		messages.success(request, "You have successfully loggedin!")
		return redirect("/books")
	return redirect("/users")

# show user method
def show_user(request, user_id):
	# user_reviews = Review.objects.filter(user=user_id)
	# my_reviews = []
	# for review in user_reviews:
	# 	if review.book not in my_reviews:
	# 		my_reviews.append(review.book)
	# 	if len(my_reviews) == 5:
	# 		break
	context = {
		"user": User.objects.get(id=user_id),
		"reviews": Review.objects.filter(user=user_id),
		# "my_reviews": my_reviews,
		"count": Review.objects.filter(user=User.objects.get(id=user_id)).count()
	}
	return render(request, "users/user.html", context)

# Logout user
def logout(request):
	request.session.clear()
	return redirect("/users/login_form")


