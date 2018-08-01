from django import forms
from django.forms import inlineformset_factory, ModelForm

from . import models
from characters.models import Character


ItemFormSet = inlineformset_factory(
    Character,
    models.Item,
    extra=0,
    fields=(
        'name',
        'is_for_sale',
        'sale_price',
    ),
    widgets={
        'name': forms.TextInput(attrs={'readonly': 'readonly'}),
    },
)


class BuyItemForm(ModelForm):
    class Meta:
        model = models.Item
        fields = ['name']