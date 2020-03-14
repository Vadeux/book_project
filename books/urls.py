from django.urls import path

from . import views

urlpatterns = [
	path('search/', views.Search.as_view(), name='search'),
	path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
	path('', views.BookListView.as_view(), name='book_list'),
	path('register/', views.RegisterFormView.as_view(), name='register'),
	path('accounts/login/', views.LoginFormView.as_view(), name='login'),
	path('logout/', views.LogoutView.as_view(), name='logout'),
	path('password-change/', views.PasswordChangeView.as_view(), name='pass-change'),
	path('filter/', views.FilterBooksView.as_view(), name='filter'),
	path('<slug:slug>/', views.BookDetailView.as_view(), name='book_detail'),
	path('review/<int:book_id>/', views.AddReview.as_view(), name='book_review'),
	path('author/<str:slug>/', views.AuthorView.as_view(), name='author_detail'),
	path('add-rating/', views.AddStarRating.as_view(), name='add_rating'),
]
