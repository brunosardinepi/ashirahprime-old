from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View

from . import forms
from . import models
from characters.models import Character
from characters.utils import get_user_character


class ItemListView(ListView):
    model = models.Item

    def get_queryset(self):
        character = get_user_character(self.request.user)
        return models.Item.objects.filter(owner=character).order_by('name')


class ItemDetailView(DetailView):
    model = models.Item


class EquipItemView(View):
    def get(self, request, *args, **kwargs):
        # assign the item to a character's gear slot based on the item type
        item = get_object_or_404(models.Item, pk=kwargs['pk'])
        character = get_user_character(item.owner.user)
        if character:
            if item.type == 'armor':
                character.armor = item
                character.save()
            elif item.type == 'weapon':
                character.weapon = item
                character.save()
            else:
                pass
        else:
            pass
        return HttpResponseRedirect('/characters/')


class UnequipItemView(View):
    def get(self, request, *args, **kwargs):
        # clear a character's gear slot based on the item type
        item = get_object_or_404(models.Item, pk=kwargs['pk'])
        character = get_user_character(item.owner.user)
        if character:
            if item.type == 'armor':
                character.armor = None
                character.save()
            elif item.type == 'weapon':
                character.weapon = None
                character.save()
            else:
                pass
        else:
            pass
        return HttpResponseRedirect('/characters/')


class SellItemsView(View):
    def get(self, request, *args, **kwargs):
        # give the user a list of their items with the option to sell them
        character = get_user_character(self.request.user)
        formset = forms.ItemFormSet(instance=character)
        return render(request,
            'items/sell_items.html',
            {'character': character, 'formset': formset}
        )

    def post(self, request, *args, **kwargs):
        character = get_user_character(self.request.user)
        formset = forms.ItemFormSet(request.POST, instance=character)
        if formset.is_valid():
            formset.save()
            return HttpResponseRedirect('/items/sell/')