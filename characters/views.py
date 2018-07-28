from django.core.exceptions import ObjectDoesNotExist
from django.shortcuts import render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.edit import CreateView, DeleteView, UpdateView

from . import forms
from . import models


class CharacterDetailView(View):
    template = 'characters/character_detail.html'

    def get(self, request, *args, **kwargs):
        try:
            character = models.Character.objects.get(user=request.user)
        except ObjectDoesNotExist:
            character = None
        return render(request, self.template, {'character': character})


class CharacterCreateView(CreateView):
    model = models.Character
    fields = ['name']

    def form_valid(self, form):
        form.instance.user = self.request.user
        return super().form_valid(form)


class CharacterUpdateView(UpdateView):
    model = models.Character
    fields = ['name']


class CharacterDeleteView(DeleteView):
    model = models.Character
    success_url = reverse_lazy('characters:character_detail')