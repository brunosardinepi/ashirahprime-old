from django.core.exceptions import ObjectDoesNotExist

from . import models


def add_credits(character, credits):
    character.wallet += credits
    character.save()


def subtract_credits(character, credits):
    character.wallet -= credits
    character.save()


def get_user_character(user):
    try:
        character = models.Character.objects.get(user=user)
    except ObjectDoesNotExist:
        character = None
    return character