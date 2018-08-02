from django.urls import path

from . import views


app_name = 'guilds'
urlpatterns = [
    path('create/', views.GuildCreateView.as_view(), name='guild_create'),
    path('search/', views.GuildSearchView.as_view(), name='guild_search'),
    path('<int:pk>/', views.GuildDetailView.as_view(), name='guild_detail'),
    path('<int:pk>/edit/', views.GuildUpdateView.as_view(), name='guild_edit'),
    path('<int:pk>/join/', views.GuildJoinView.as_view(), name='guild_join'),
    path('<int:pk>/leave/', views.GuildLeaveView.as_view(), name='guild_leave'),
    path('', views.GuildListView.as_view(), name='guild_list'),
]