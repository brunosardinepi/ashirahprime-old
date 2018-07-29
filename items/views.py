from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View

from . import models
from characters.models import Character
from characters.utils import get_user_character


class ItemListView(ListView):
    model = models.Item

    def get_queryset(self):
        return models.Item.objects.filter(user=self.request.user).order_by('name')


class ItemDetailView(DetailView):
    model = models.Item


class EquipItemView(View):
    def get(self, request, *args, **kwargs):
        # assign the item to a character's gear slot based on the item type
        item = get_object_or_404(models.Item, pk=kwargs['item_pk'])
        character = get_user_character(item.user)
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