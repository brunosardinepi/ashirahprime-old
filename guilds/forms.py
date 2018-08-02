from django import forms
from django.forms import ModelForm

from . import models


class GuildForm(ModelForm):
    class Meta:
        model = models.Guild
        fields = ['name', 'is_public']