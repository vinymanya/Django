# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from django.db import models

from ..users.models import User


# manager for the book model
class BookManager(models.Manager):
	def validate_book(self, post_data):
		errors = {}
		# check for emptiness of fields
		for field, value in post_data.iteritems():
			if field != "csrfmiddlewaretoken" and field != "authors" and field != "rating":
				if len(value) < 1:
					errors[field] = "{} field is required!".format(field.replace('_', ''))
			if field == "authors":
				if len(value) > 1 and field != "":
					errors[field] = "Only one {} field maybe specified".format(field.replace("s", ""))
			# Check for review 'review' field
			if field == "review":
				if field not in errors and len(value) < 1:
					errors[field] = "Please leave a {}".format(field)
			# Check for rating
			if field == "rating":
				if field not in errors and value == "":
					errors[field] = "Please select {}".format(field)
		return errors

	def new_record(self, request, post_data):
			# Check if the 'title' already exist in db
	        book_list = []
	        books = Book.objects.all()
	        for book in books:
	            if book.title not in book_list:
	                book_list.append(book.title)
	        if post_data["title"] not in book_list:  
	            Book.objects.create(
	            	title=post_data["title"], 
	            	author=post_data["author"] or post_data.get("authors"), 
	            	user_id=request.session["user_id"]
	            )
	            Review.objects.create(
	            	content=post_data["review"], 
	            	rating=post_data["rating"], 
	            	user_id=request.session["user_id"], 
	            	book_id=Book.objects.last().id
	            )
	            book_id = Book.objects.last().id 
	            return book_id 
	        else: # If the 'title' already esists then we only save the review
	            Review.objects.create(
	            	content=post_data["review"], 
	            	rating=post_data["rating"], 
	            	user_id=request.session["user_id"], 
	            	book_id=Book.objects.get(title = post_data["title"]).id)
	            book_id = Book.objects.get(title=post_data["title"]).id
	            return book_id


# manager for the review model
class ReviewManager(models.Manager):
	def validate_review(self, post_data):
		errors = {}
		# validate the review field
		for field, value in post_data.iteritems():
			if field == "review":
				if field not in errors and len(value) < 1:
					errors[field] = "Please leave a {}".format(field)
			if field == "rating":
				if field not in errors and value == "":
					errors[field] = "{} is required".format(field)
		return errors

	# Create a new review
	def new_review(self, request, book_id, user_id):
		Review.objects.create(
				content = request.POST["review"],
				rating = request.POST.get('rating'),
				user = User.objects.get(id=user_id),
				book = Book.objects.get(id=book_id)
			) 

# Create your models here.
class Book(models.Model):
    title = models.CharField(max_length=255)
    author = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="books")
    objects = BookManager()

    def __repr__(self):
    	print "<Book Object: Title: {}, Author: {}, User: {}".format(self.title, self.author, self.user.name)


class Review(models.Model):
    content = models.TextField()
    rating = models.CharField(max_length=255)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, related_name="reviews")
    book = models.ForeignKey(Book, related_name="reviews")

    objects = ReviewManager()

    def __str__(self):
    	print "<Review Object: Content: {}, Rating: {}, User: {}, Book: {}".format(self.content, self.rating, self.user.name, self.book.title)
