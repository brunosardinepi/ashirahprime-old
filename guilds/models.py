import uuid

from django.db import models
from django.urls import reverse


class Guild(models.Model):
    creator = models.ForeignKey(
        'characters.Character',
        null=True,
        on_delete=models.SET_NULL,
    )
    name = models.CharField(max_length=255)
    is_public = models.BooleanField(default=True)
    public_url = models.CharField(max_length=255, unique=True, default=uuid.uuid4)
    members = models.ManyToManyField('characters.Character', related_name='members')

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('guilds:guild_detail', kwargs={'pk': self.pk})

