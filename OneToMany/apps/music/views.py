# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from .models import Artist, Album
from django.shortcuts import render, redirect, HttpResponse

# Create your views here.

def index(request):
	context = {
		"artists": Artist.objects.all(),
		"albums": Album.objects.all()
	}
	return render(request, "music/index.html", context)

def create_artist(request):
	the_artist = Artist.objects.create(
			name = request.POST["artist"]
		)
	return redirect("/artists/{}".format(the_artist.id))

def show_artist(request, artist_id):
	context = {
		"artist": Artist.objects.get(id=artist_id)
	}
	return render(request, "music/show_artist.html", context)

def create_album(request):
	the_artist = Artist.objects.get(id=request.POST["artist_id"])
	the_album = Album.objects.create(
			name = request.POST["album_name"],
			release_year = request.POST["release_year"],
			label = request.POST["label"],
			artist = the_artist
		)
	return redirect("/albums/{}".format(the_album.id))

def show_album(request, album_id):
	context = {
		"album": Album.objects.get(id = album_id)
	}
	return render(request, "music/show_album.html", context)

