from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Message(models.Model):
    owner = models.ForeignKey(User, on_delete=models.CASCADE)
    sender = models.ForeignKey(
        'characters.Character',
        null=True,
        on_delete=models.SET_NULL,
        related_name='sender',
    )
    recipient = models.ForeignKey(
        'characters.Character',
        null=True,
        on_delete=models.SET_NULL,
        related_name='recipient',
    )
    subject = models.CharField(max_length=255, blank=True)
    body = models.TextField()
    date = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)
    is_deleted = models.BooleanField(default=False)
    previous_message = models.ForeignKey('self', null=True, on_delete=models.SET_NULL)

    def __str__(self):
        return "from: {}; to: {}; body: {}".format(sender, recipient, body[:25])

    def get_absolute_url(self):
        return reverse('mail:message_detail', pk=self.pk)