from django.shortcuts import render
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Book


# Create your views here.


class BookListView(ListView):
	"""List of books."""
	model = Book
	queryset = Book.objects.filter(draft=False)


class BookDetailView(DetailView):
	model = Book
	slug_field = 'url'
