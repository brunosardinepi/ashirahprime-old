from django.http import HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.urls import reverse_lazy
from django.views import View
from django.views.generic.detail import DetailView
from django.views.generic.edit import CreateView, DeleteView, UpdateView
from django.views.generic.list import ListView

from . import forms
from . import models
from characters.utils import get_user_character


class GuildDetailView(View):
    def get(self, request, *args, **kwargs):
        guild = get_object_or_404(models.Guild, pk=kwargs['pk'])
        members = guild.members.all()
        return render(request,
            'guilds/guild_detail.html',
            {'guild': guild, 'members': members},
        )


class GuildListView(ListView):
    model = models.Guild
    template_name = "guilds/guild_list.html"

    def get_queryset(self):
        character = get_user_character(self.request.user)
        return character.guilds()


class GuildSearchView(ListView):
    model = models.Guild
    template_name = "guilds/guild_search.html"


class GuildCreateView(View):
    def get(self, request, *args, **kwargs):
        form = forms.GuildForm()
        return render(request, 'guilds/guild_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.GuildForm(request.POST)
        if form.is_valid():
            guild = form.save(commit=False)
            character = get_user_character(self.request.user)
            guild.creator = character
            guild.save()
            guild.members.add(character)
            return HttpResponseRedirect('/guilds/')


class GuildJoinView(View):
    def get(self, request, *args, **kwargs):
        guild = get_object_or_404(models.Guild, pk=kwargs['pk'])
        form = forms.GuildForm(instance=guild)
        return render(request,
            'guilds/guild_join.html',
            {'guild': guild, 'form': form}
        )

    def post(self, request, *args, **kwargs):
        guild = get_object_or_404(models.Guild, pk=kwargs['pk'])
        form = forms.GuildForm(request.POST, instance=guild)
        if form.is_valid():
            character = get_user_character(self.request.user)
            guild.members.add(character)
            return HttpResponseRedirect('/guilds/')


class GuildLeaveView(View):
    def get(self, request, *args, **kwargs):
        guild = get_object_or_404(models.Guild, pk=kwargs['pk'])
        form = forms.GuildForm(instance=guild)
        return render(request,
            'guilds/guild_leave.html',
            {'guild': guild, 'form': form}
        )

    def post(self, request, *args, **kwargs):
        guild = get_object_or_404(models.Guild, pk=kwargs['pk'])
        form = forms.GuildForm(request.POST, instance=guild)
        if form.is_valid():
            character = get_user_character(self.request.user)
            guild.members.remove(character)
            return HttpResponseRedirect('/guilds/')


class GuildUpdateView(UpdateView):
    model = models.Guild
    fields = ['name', 'is_public']