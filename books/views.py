from django.shortcuts import render, redirect, get_object_or_404
from django.views.generic import ListView, DetailView
from django.views.generic.base import View

from .models import Book, Category
from .forms import ReviewForm


# Create your views here.


class BookListView(ListView):
	"""List of books."""
	model = Book
	queryset = Book.objects.filter(draft=False)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['last_books'] = Book.objects.order_by('id')[:3]
		context['last_last_books'] = Book.objects.order_by('id')[3:7]
		context['categories'] = Category.objects.all()
		return context


class BookDetailView(DetailView):
	"""One book."""
	model = Book
	slug_field = 'url'

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['categories'] = Category.objects.all()
		return context


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
