from django.urls import path

from . import views


app_name = 'forum'
urlpatterns = [
    path('<int:pk>/', views.ForumDetailView.as_view(), name='forum_detail'),
    path('<int:pk>/post/create/', views.PostCreateView.as_view(), name='post_create'),
    path('<int:forum_pk>/post/<int:post_pk>/',
        views.PostDetailView.as_view(), name='post_detail'),
    path('<int:forum_pk>/post/<int:post_pk>/comment/create/',
        views.CommentCreateView.as_view(), name='comment_create'),
    path('', views.ForumListView.as_view(), name='forum_list'),
]