from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic import ListView, DetailView
from django.views.generic.edit import FormView
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from django.http import HttpResponseRedirect
from django.views.generic.base import View
from django.contrib.auth import logout
from django.contrib.auth.forms import PasswordChangeForm


from .models import Book, Category, Genre, Author
from .forms import ReviewForm


# Create your views here.
class GenreMixin():
	"""For list of genres in side bar."""

	def get_genres(self):
		return Genre.objects.all()


class BookListView(GenreMixin, ListView):
	"""List of books."""
	model = Book
	queryset = Book.objects.filter(draft=False)

	def get_context_data(self, *args, **kwargs):
		context = super().get_context_data(*args, **kwargs)
		context['last_books'] = Book.objects.order_by('id')[:3]
		context['last_last_books'] = Book.objects.order_by('id')[3:7]
		context['categories'] = Category.objects.all()
		return context


class BookDetailView(GenreMixin, DetailView):
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


class AuthorView(GenreMixin, DetailView):
	"""Author page."""
	model = Author
	template_name = 'books/author.html'
	slug_field = 'name'


class FilterBooksView(GenreMixin, ListView):
	"""Book filter."""

	def get_queryset(self):
		queryset = Book.objects.filter(
			genres__in=self.request.GET.getlist('genre')
		).distinct()
		return queryset


class RegisterFormView(FormView):
	form_class = UserCreationForm
	success_url = '/'
	template_name = 'books/reg/register.html'

	def form_valid(self, form):
		form.save()
		return super(RegisterFormView, self).form_valid(form)


class LoginFormView(FormView):
	form_class = AuthenticationForm
	template_name = "books/reg/login.html"
	success_url = 'http://127.0.0.1:8000/'

	def form_valid(self, form):
		self.user = form.get_user()
		login(self.request, self.user)
		return super(LoginFormView, self).form_valid(form)


class LogoutView(View):
	def get(self, request):
		logout(request)
		return HttpResponseRedirect('/')


class PasswordChangeView(FormView):
	form_class = PasswordChangeForm
	template_name = 'books/reg/password_change_form.html'
	success_url = '/'

	def get_form_kwargs(self):
		kwargs = super(PasswordChangeView, self).get_form_kwargs()
		kwargs['user'] = self.request.user
		if self.request.method == 'POST':
			kwargs['data'] = self.request.POST
		return kwargs

	def form_valid(self, form):
		form.save()
		return super(PasswordChangeView, self).form_valid(form)


