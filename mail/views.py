from django.shortcuts import redirect, render
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views import View

from . import forms
from . import models
from characters.utils import get_user_character


class MessageListView(View):
    def get(self, request, *args, **kwargs):
        character = get_user_character(self.request.user)
        sent_messages = models.Message.objects.filter(
            sender=character).order_by('date')
        received_messages = models.Message.objects.filter(
            recipient=character).order_by('date')

        return render(request,
            'mail/message_list.html',
            {
                'character': character,
                'sent_messages': sent_messages,
                'received_messages': received_messages,
            }
        )


class MessageDetailView(DetailView):
    model = models.Message


class MessageCreateView(View):
    def get(self, request, *args, **kwargs):
        form = forms.MessageForm()
        return render(request, 'mail/message_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)
            character = get_user_character(self.request.user)
            message.sender = character
            message.save()
            return redirect('mail:message_list')