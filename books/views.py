from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Book
from .forms import ReviewForm


# Create your views here.


class BookListView(ListView):
	"""List of books."""
	model = Book
	queryset = Book.objects.filter(draft=False)


class BookDetailView(DetailView):
	"""One book."""
	model = Book
	slug_field = 'url'


class AddReview(View):
	"""For sending reviews."""

	def post(self, request, book_id):
		form = ReviewForm(request.POST)
		book = get_object_or_404(Book, id=book_id)
		if form.is_valid():
			form = form.save(commit=False)
			if request.POST.get('parent', None):
				form.parent_id = int(request.POST.get('parent'))
			form.book = book
			form.save()
		return redirect(book.get_absolute_url())
