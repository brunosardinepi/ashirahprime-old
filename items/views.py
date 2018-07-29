from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View

from . import models
from characters.models import Character


class ItemListView(ListView):
    model = models.Item

    def get_queryset(self):
        return models.Item.objects.filter(user=self.request.user).order_by('name')


class ItemDetailView(DetailView):
    model = models.Item

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        try:
            character = Character.objects.get(user=self.request.user)
        except ObjectDoesNotExist:
            character = None
        context['character'] = character
        return context


class EquipItemView(View):
    def get(self, request, *args, **kwargs):
        # assign the item to a character's gear slot based on the item type
        character = get_object_or_404(Character, pk=kwargs['character_pk'])
        item = get_object_or_404(models.Item, pk=kwargs['item_pk'])
        if item.type == 'armor':
            character.armor = item
            character.save()
        elif item.type == 'weapon':
            character.weapon = item
            character.save()
        else:
            pass
        return HttpResponseRedirect('/characters/')