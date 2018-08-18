# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.shortcuts import render, redirect
from django.contrib import messages

from ..users.models import User
from .models import Book, Review


# Create your views here.
def dashboard(request):
	try:
		request.session["user_id"]
	except KeyError:
		return redirect("/users/login_form")

	list_of_books_ids = Review.objects.all().order_by("-created_at")[:3].values_list("book_id", flat=True)
	other_books = Book.objects.exclude(id__in=list_of_books_ids)


	# # Take the last three books with reviews
	all_reviews = Review.objects.all()
	recent_books = []

	for review in all_reviews:
		if review.book.title not in recent_books:
			recent_books.append(review.book.title)
		if len(recent_books) == 3:
			break

	context = {
	   "user": User.objects.get(id=request.session["user_id"]),
	   "books": Book.objects.all(),
	   "reviews": Review.objects.all().order_by("-created_at")[:3], # The last three reviews,
	   "other_books": other_books,
	   "recent_books": recent_books
	}
	return render(request, "books/dashboard.html", context)

# add method
def add(request):
	# Get all books
	books = Book.objects.all()
	# filter authors from books
	authors_list = []
	for book in books:
		if book.author not in authors_list:
			authors_list.append(book.author)

	context = {
		"authors_list": authors_list
	}
	return render(request, "books/add_book.html", context)

# Add review method
def add_review(request, book_id, user_id):
	errors = Review.objects.validate_review(request.POST)
	if len(errors):
		for field, error_msg in errors.iteritems():
			messages.error(request, error_msg, extra_tags=field)
		return redirect("/books/{}".format(book_id))
	# create a new review
	Review.objects.new_review(request, book_id, user_id)
	return redirect("/books/{}".format(book_id))


# method that handles book creating
def create(request):
    if request.method == "POST":
        errors = Book.objects.validate_book(request.POST)
        print(errors)
        if len(errors):
            for tag, error_msg in errors.iteritems():
                messages.error(request, error_msg, extra_tags=tag)
            return redirect("/books/add")
        # Create a new book record
        book_id = Book.objects.new_record(request, request.POST)
        return redirect("/books/{}".format(book_id))


# method that shows book detail including reviews
def book_detail(request, book_id):
	context = {
		"book": Book.objects.get(id=book_id),
		"reviews": Review.objects.filter(book=book_id).order_by("-created_at")[:5] # Retrieve the reviews that belongs to this book
	}
	return render(request, "books/show_book.html", context)


# Method for deleting a book
def delete_review(request, book_id, review_id):
	# Delete the review with this id
	review = Review.objects.get(id=review_id)
	review.delete()
	return redirect("/books/{}".format(book_id))
	















	
