from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    armor = models.ForeignKey(
        'items.Item',
        on_delete=models.SET_NULL,
        related_name='armor',
        null=True,
        blank=True,
    )
    weapon = models.ForeignKey(
        'items.Item',
        on_delete=models.SET_NULL,
        related_name='weapon',
        null=True,
        blank=True,
    )
    wallet = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('characters:character_detail')