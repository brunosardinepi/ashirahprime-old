from django.forms import ModelForm

from . import models


class CharacterCreateForm(ModelForm):
    class Meta:
        model = models.Character
        fields = ['name']