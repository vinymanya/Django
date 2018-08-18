# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import User
from django.contrib import messages
from functools import wraps

# Create your views here.
def index(request):
	return render(request, "signup/index.html") 


def login(request):
	if request.method == "POST":
		result = User.objects.validateLogin(request.POST) # This will either return [errors] or [user]
		if type(result) == list:
			for error in result:
				messages.error(request, error)
				return redirect("/")
				#load login the user
		request.session["user_id"] = result.id
		messages.success(request, "You have successfully logged in!")
		return redirect("/users/success")
	return redirect("/")

		
def register(request):
	if request.method == "POST":
		result = User.objects.validateRegister(request.POST)
		if type(result) == list:
			for error in result:
				messages.error(request, error)
			return redirect("/")
		request.session["user_id"] = result.id
		messages.success(request, "You have successfully registered!")
		return redirect("/users/success")
	return redirect("/")


#decorator definition
def is_logged_in(request, f):
	@wraps(f)
	def wrap(*args, **kwargs):
		if "user_id" in request.session:
			return f(*args, **kwargs)
		else:
			messages.danger(request, "Unauthorized!, please loggin!")
			return redirect("/")
	return wrap


def success(request):
	try:
		request.session["user_id"]
	except KeyError:
		return redirect("/")
	context = {
		"user": User.objects.get(id=request.session["user_id"])
	}
	return render(request, "signup/success.html", context)


def logout(request):
	request.session.clear()
	return redirect("/")



		