# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse
from .models import Author, Book

# Create your views here.
def index(request):
	context = {
		"authors": Author.objects.all()
	}
	return render(request, "books/index.html", context)
