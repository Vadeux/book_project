from django.urls import path

from . import views

urlpatterns = [
	path('create/', views.order_create, name='order_create'),
	path('all/', views.OrderListView.as_view(), name='orders_list'),
]
