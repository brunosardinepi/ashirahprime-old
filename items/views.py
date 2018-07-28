from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from . import models


class ItemListView(ListView):
    model = models.Item

    def get_queryset(self):
        return models.Item.objects.filter(user=self.request.user).order_by('name')


class ItemDetailView(DetailView):
    model = models.Item
