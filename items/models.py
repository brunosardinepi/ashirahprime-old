from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Item(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    TYPE = (
        ('armor', 'armor'),
        ('weapon', 'weapon'),
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE,
        default='armor',
    )

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items:item_detail')