from datetime import datetime

from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.contrib.auth.models import User
from django.http import HttpResponseRedirect
from django.shortcuts import render
from django.views.generic import ListView, DetailView

# Create your views here.
from .models import Post


class PostListView(ListView):
	"""List of posts."""
	model = Post
	template_name = 'blog/blog_list.html'


class PostDetailView(LoginRequiredMixin, DetailView):
	"""One post."""
	model = Post
	template_name = 'blog/blog_detail.html'


def admin(request):
	"""add posts."""
	message = None
	if "message" in request.GET:
		message = request.GET["message"]
	# создание HTML-страницы по шаблону admin.html
	# с заданными параметрам message
	return render(
		request,
		"admin.html",
		{
			"message": message,
		}
	)


def post_post(request):
	# защита от добавления загадок неадминистраторами
	author = request.user
	if not (author.is_authenticated and author.is_staff):
		return HttpResponseRedirect("/admin")
	# добавление загадки
	pst = Post()
	pst.title = request.POST.get('title', True)
	pst.text = request.POST.get('text', True)
	pst.reg_date = datetime.now()
	pst.save()

	return HttpResponseRedirect('http://127.0.0.1:8000/blog/' + str(pst.id))
