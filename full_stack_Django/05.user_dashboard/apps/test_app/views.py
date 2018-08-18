# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect, HttpResponse
from .models import User, User2, New_message, Comment
from django.contrib import messages



# Create your views here.
def index(request):
	return render(request, "test_app/index.html")

def signin(request):
	return render(request, "test_app/signin.html")

def login(request):
	if request.method == "POST":
		result = User.objects.validateLogin(request.POST) #This will either return [errors] or [user]
		if type(result) == list:
			for error in result:
				# messages.error(request, error)
				return redirect("/signin")
				#load login the user
		request.session["user_id"] = result.id
		# messages.success(request, "You have successfully logged in!")
		return redirect("/dashboard")
	return redirect("/signin")

		
def register(request):
	
	if request.method == "POST":
		result = User.objects.validateRegister(request.POST)
		if type(result) == list:
			for error in result:
				# messages.error(request, error)
				return redirect("/signin")
		request.session["user_id"] = result.id
		# messages.success(request, "You have successfully registered!")
		return redirect("/dashboard")
	return redirect("/signin")


def dashboard(request):
	try:
		request.session["user_id"]
	except KeyError:
		return redirect("/signin")
	context = {
		"user": User.objects.get(id=request.session["user_id"]),
		"users": User2.objects.all()
	}
	return render(request, "test_app/dashboard.html", context)

def logout(request):
	request.session.clear()
	return redirect("/signin")


#Semi-restful-users
def new_user(request):
	return render(request, "test_app/create.html")

def create(request):
	errors = User2.objects.validate(request.POST)
	print errors
	if len(errors):
		for field, message in errors.iteritems():
			error(request, message, extra_tags=field)
		return redirect("/users/new")

	else:
		#create a new users
		User2.objects.create(
			first_name = request.POST["first_name"],
			last_name = request.POST["last_name"],
			email = request.POST["email"],
			desc = request.POST["desc"]

		)
		return redirect("/dashboard")

def show(request, id):
	context = {
		"user": User2.objects.get(id=id), #same as "SELECT * FROM users WHERE id = :id"
		"messages": New_message.objects.all(), # same as "SELECT * FROM Message"
		"comments": Comment.objects.all()
	}
	return render(request, "test_app/show.html", context)

def edit_user(request, id):
	context = {
		"user": User2.objects.get(id=id)
	}
	return render(request, "test_app/update.html", context)

def update(request, id):
	errors = User2.objects.validate(request.POST)
	if len(errors):
		for field, message in errors.iteritems():
			error(request, message, extra_tags= field)
		return redirect("/users/{}/edit".format(id))
	else:
		update_user = User2.objects.get(id=id)
		update_user.first_name = request.POST["first_name"]
		update_user.last_name = request.POST["last_name"]
		update_user.email = request.POST["email"]
		update_user.desc = request.POST["desc"]
		update_user.save()
		return redirect("/dashboard")

def confirm(request, id):
	context ={
		"user": User2.objects.get(id=id)
	}
	return render(request, "test_app/confirm.html", context)

def delete(request, id):
	User2.objects.get(id=id).delete()
	return redirect("/dashboard")

def messages(request, id):
	#Create messages using ORM:
	messages = New_message.objects.create(message=request.POST["message_id"])
	return redirect("/users/{}".format(id))

def comments(request, id):
	if request.method == " POST":
		message = New_message.objects.get(id=id)
		comment = Comment.objects.create(comment=request.POST["comment"], message=message.id)
	return redirect("/users/{}".format(comment.id))

