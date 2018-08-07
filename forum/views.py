from django.shortcuts import get_object_or_404, redirect, render
from django.views import View

from . import forms
from . import models


class ForumListView(View):
    def get(self, request, *args, **kwargs):
        forums = models.Forum.objects.all().order_by('name')
        return render(request, 'forum/forum_list.html', {'forums': forums})


class ForumDetailView(View):
    def get(self, request, *args, **kwargs):
        forum = get_object_or_404(models.Forum, pk=kwargs['pk'])
        posts = models.Post.objects.filter(forum=forum).order_by('-date')
        return render(request,
            'forum/forum_detail.html',
            {'forum': forum, 'posts': posts},
        )


class PostCreateView(View):
    def get(self, request, *args, **kwargs):
        forum = get_object_or_404(models.Forum, pk=kwargs['pk'])
        form = forms.PostCreateForm()
        return render(request,
            'forum/post_create.html',
            {'forum': forum, 'form': form}
        )

    def post(self, request, *args, **kwargs):
        forum = get_object_or_404(models.Forum, pk=kwargs['pk'])
        form = forms.PostCreateForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)

            # assign it to the forum
            post.forum = forum

            # set the user
            post.user = request.user

            post.save()
            return redirect('forum:post_detail', forum_pk=forum.pk, post_pk=post.pk)


class PostDetailView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['post_pk'])
        return render(request, 'forum/post_detail.html', {'post': post})


class CommentCreateView(View):
    def get(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['post_pk'])
        form = forms.CommentCreateForm()
        return render(request,
            'forum/comment_create.html',
            {'post': post, 'form': form}
        )

    def post(self, request, *args, **kwargs):
        post = get_object_or_404(models.Post, pk=kwargs['post_pk'])
        form = forms.CommentCreateForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)

            # assign it to the post
            comment.post = post

            # set the user
            comment.user = request.user

            comment.save()
            return redirect('forum:post_detail',
                forum_pk=post.forum.pk,
                post_pk=post.pk,
            )