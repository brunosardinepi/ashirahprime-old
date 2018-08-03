from django.shortcuts import get_object_or_404, redirect, render
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
            sender=character).order_by('-date')
        received_messages = models.Message.objects.filter(
            recipient=character).order_by('-date')

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

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['character'] = get_user_character(self.request.user)
        return context


class MessageCreateView(View):
    def get(self, request, *args, **kwargs):
        form = forms.MessageForm()
        return render(request, 'mail/message_create.html', {'form': form})

    def post(self, request, *args, **kwargs):
        form = forms.MessageForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            # set sender to current user's character
            character = get_user_character(self.request.user)
            message.sender = character

            message.save()
            return redirect('mail:message_list')


class MessageReplyView(View):
    def get(self, request, *args, **kwargs):
        # get previous message based on the url pk
        previous_message = get_object_or_404(models.Message, pk=kwargs['pk'])

        form = forms.MessageReplyForm()
        return render(request,
            'mail/message_reply.html',
            {'form': form, 'previous_message': previous_message}
        )

    def post(self, request, *args, **kwargs):
        form = forms.MessageReplyForm(request.POST)
        if form.is_valid():
            message = form.save(commit=False)

            # get previous message based on the url pk
            previous_message = get_object_or_404(models.Message, pk=kwargs['pk'])
            message.previous_message = previous_message

            # set sender to current user's character
            character = get_user_character(self.request.user)
            message.sender = character

            # carry over immutable fields since this is a reply
            message.recipient = previous_message.sender
            message.subject = previous_message.subject

            message.save()
            return redirect('mail:message_list')