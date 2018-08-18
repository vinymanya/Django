# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
# from time import gmtime, strftime
from .models import User
from django.contrib.messages import error

# Create your views here.
def index(request):
	# Select all users from db
	context = {
		"users": User.objects.all().order_by('-created_at')
	}
	return render(request, "usersapp/index.html", context)

def new_user(request):
	return render(request, "usersapp/create.html")

def create(request):
	errors = User.objects.validate(request.POST)
	if len(errors):
		for field, message in errors.iteritems():
			error(request, message, extra_tags = field)
		return redirect("/users/new")

	else:
		#create a new users
		User.objects.create(
			first_name = request.POST["first_name"],
			last_name = request.POST["last_name"],
			email = request.POST["email"]

		)
		return redirect("/users")

def show(request, id):
	context = {
		"user": User.objects.get(id=id)
	}
	#same as "SELECT * FROM users WHERE id = :id"
	return render(request, "usersapp/show.html", context)

def edit_user(request, id):
	context = {
		"user": User.objects.get(id=id)
	}
	return render(request, "usersapp/update.html", context)

def update(request, id):
	errors = User.objects.validate(request.POST)
	print errors
	if len(errors):
		for field, message in errors.iteritems():
			error(request, message, extra_tags = field)
		return redirect("/users/{}/edit".format(id))
	else:
		update_user = User.objects.get(id=id)
		update_user.first_name = request.POST["first_name"]
		update_user.last_name = request.POST["last_name"]
		update_user.email = request.POST["email"]
		update_user.save()
		return redirect("/users/{}".format(id))

def delete(request, id):
	User.objects.get(id=id).delete()
	return redirect("/users")

