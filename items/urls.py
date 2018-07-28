from django.urls import path

from . import views


app_name = 'items'
urlpatterns = [
    path('<int:pk>/', views.ItemDetailView.as_view(), name='item_detail'),
    path('', views.ItemListView.as_view(), name='item_list'),
]