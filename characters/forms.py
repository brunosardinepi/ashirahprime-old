from django.forms import ModelForm

from . import models


class CharacterForm(ModelForm):
    class Meta:
        model = models.Character
        fields = ['name']