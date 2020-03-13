from django.urls import path

from . import views

urlpatterns = [
	path('', views.PostListView.as_view(), name='post_list'),
	path('<int:pk>/', views.PostDetailView.as_view(), name='post_detail'),
	path('admin/', views.admin, name='admin'),
	path('add_post/', views.post_post, name='add_post'),

]
