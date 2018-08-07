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
            owner=request.user, sender=character).order_by('-date')
        received_messages = models.Message.objects.filter(
            owner=request.user, recipient=character).order_by('-date')

        return render(request,
            'mail/message_list.html',
            {
                'character': character,
                'sent_messages': sent_messages,
                'received_messages': received_messages,
            }
        )


class MessageDetailView(View):
    def get(self, request, *args, **kwargs):
        # context for template
        character = get_user_character(self.request.user)
        message = get_object_or_404(models.Message, pk=kwargs['pk'])

        # set message to 'read' if this is the first time opening
        if message.is_read == False:
            message.is_read = True
            message.save()

        return render(request,
            'mail/message_detail.html',
            {'character': character, 'message': message},
        )


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

            # set owner to current user
            message.owner = request.user

            message.save()

            # create a copy to be shown in the recipient's inbox
            message.pk = None
            message.owner = message.recipient.user
            message.save()

            return redirect('mail:message_list')
        else:
            print(form.errors)


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

            # set owner to current user
            message.owner = request.user

            # carry over immutable fields since this is a reply
            message.recipient = previous_message.sender
            message.subject = previous_message.subject

            message.save()

            # create a copy to be shown in the recipient's inbox
            message.pk = None
            message.owner = message.recipient.user
            message.save()

            return redirect('mail:message_list')


class MessageDeleteView(View):
    def get(self, request, *args, **kwargs):
        message = get_object_or_404(models.Message, pk=kwargs['pk'])
        # check if this user is the message owner before deleting
        if message.owner == request.user:
            message.delete()
            return redirect('mail:message_list')