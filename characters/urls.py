from django.urls import path

from . import views


app_name = 'characters'
urlpatterns = [
    path('create/', views.CharacterCreateView.as_view(), name='character_create'),
    path('<int:pk>/delete/', views.CharacterDeleteView.as_view(), name='character_delete'),
    path('', views.CharacterDetailView.as_view(), name='character_detail'),
]