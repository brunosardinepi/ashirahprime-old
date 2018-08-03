from django import forms
from django.forms import ModelForm

from . import models


class MessageForm(ModelForm):
    class Meta:
        model = models.Message
        fields = [
            'recipient',
            'subject',
            'body',
        ]

class MessageReplyForm(ModelForm):
    class Meta:
        model = models.Message
        fields = [
            'body',
        ]