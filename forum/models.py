from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Forum(models.Model):
    name = models.CharField(max_length=255)
    date = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
#        return reverse('forum:forum_detail', pk=self.pk)
        pass


class Post(models.Model):
    forum = models.ForeignKey(Forum, on_delete=models.CASCADE)
    title = models.CharField(max_length=255)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{}: {}".format(self.user, self.title[:10])

    def get_absolute_url(self):
#        return reverse('forum:post_detail', pk=self.pk)
        pass

    def comments(self):
        return Comment.objects.filter(post=self).order_by('date')


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    user = models.ForeignKey(User, null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "{}: {}".format(self.user, self.body[:10])

    def get_absolute_url(self):
#        return reverse('forum:comment_detail', pk=self.pk)
        pass