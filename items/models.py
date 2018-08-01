from django.db import models
from django.urls import reverse


class Item(models.Model):
    ARMOR = 'armor'
    WEAPON = 'weapon'
    TYPE = (
        (ARMOR, 'Armor'),
        (WEAPON, 'Weapon'),
    )
    type = models.CharField(
        max_length=10,
        choices=TYPE,
        default=ARMOR,
    )

    owner = models.ForeignKey(
        'characters.Character',
        on_delete=models.CASCADE,
        blank=True,
        null=True,
    )
    name = models.CharField(max_length=255)
    is_for_sale = models.BooleanField(default=False)
    sale_price = models.BigIntegerField(default=0)

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse('items:item_detail')