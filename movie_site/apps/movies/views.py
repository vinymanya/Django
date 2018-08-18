# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages

from .models import Movie

# Create your views here.

# mthod to hanle movies
def movies(request):
	# Retrieve all movies
	context = {
		"movies": Movie.objects.all()
	}
	return render(request, "movies/movies.html", context)


# Method that handles movie creation
def create_movie(request):
	if request.method == "POST":
		errors = Movie.objects.validate_movie(request.POST)
		if errors:
			for error_msg in errors:
				messages.error(request, error_msg)
			return redirect("/movies/title")
		# create a movie
		Movie.objects.create(title=request.POST["title"])
		return redirect("/actors")

# Method that handles movie deletion
def delete_movie(request, movie_id):
	the_movie = Movie.objects.get(id=movie_id)
	the_movie.delete()
	return redirect("/movies/title")


