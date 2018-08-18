# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Actor
from ..movies.models import Movie

# Create your views here.
def index(request):
	# Retrieve all actors
	context = {
		"actors": Actor.objects.all()
	}
	return render(request, "actors/index.html", context)


# Method to add an actor
def create(request):
	if request.method == "POST":
		errors = Actor.objects.validate_actor(request.POST)
		if errors:
			for error_msg in errors:
				messages.error(request, error_msg)
			return redirect("/actors")
		# Add actor to db
		Actor.objects.create(
				first_name = request.POST["first_name"],
				last_name = request.POST["last_name"],
				dob = request.POST["dob"]
			)
		return redirect("/actors")

# Method to delete actor
def delete_actor(request, actor_id):
	actor = Actor.objects.get(id=actor_id)
	actor.delete()
	return redirect("/actors")

# Method that shows actor's details
def show_actor(request, actor_id):
	# Get all the movies by this actor
	movies_by_actor = Actor.objects.get(id=actor_id).movies.all()
	# Filter data to avoid listing already selected movies 
	movie_ids = []
	for movie in movies_by_actor:
		movie_ids.append(movie.id)

	context = {
		"actor": Actor.objects.get(id=actor_id),
		"movies": Movie.objects.all(),
		"movie_ids":movie_ids
	}
	return render(request, "actors/show.html", context)

# add actor to movie
def add_to_movie(request, actor_id):
	the_actor = Actor.objects.get(id=actor_id)
	the_movie = Movie.objects.get(id=request.POST["movie_id"])
	# This is how you create the many to many relationship with the .add() method
	the_movie.actors.add(the_actor)
	return redirect("/actors/{}".format(actor_id))


# Method that remove the relationship
def remove_from_movie(request, actor_id, movie_id):
	the_actor = Actor.objects.get(id=actor_id)
	the_movie = Movie.objects.get(id=movie_id)
	# This is how you remove a many to many relationship
	the_actor.movies.remove(the_movie)
	return redirect("/actors/{}".format(actor_id))





