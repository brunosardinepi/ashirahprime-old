from django.urls import path

from . import views


app_name = 'mail'
urlpatterns = [
    path('<int:pk>/', views.MessageDetailView.as_view(), name='message_detail'),
    path('create/', views.MessageCreateView.as_view(), name='message_create'),
    path('', views.MessageListView.as_view(), name='message_list'),
]