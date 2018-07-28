from django.contrib.auth.models import User
from django.db import models
from django.urls import reverse


class Character(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    name = models.CharField(max_length=255)

    def get_absolute_url(self):
#        return reverse('characters:character_detail', kwargs={'pk': self.pk})
        return reverse('characters:character_detail')