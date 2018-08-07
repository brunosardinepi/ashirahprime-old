from django import forms
from django.forms import ModelForm

from . import models


class PostCreateForm(ModelForm):
    class Meta:
        model = models.Post
        fields = ['title', 'body']

class CommentCreateForm(ModelForm):
    class Meta:
        model = models.Comment
        fields = ['body']