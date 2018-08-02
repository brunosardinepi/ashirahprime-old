from django.core.exceptions import ObjectDoesNotExist

from . import models


def complete_transaction(buyer, item):
    # the credit amount is the item sale price
    credits = item.sale_price

    # make sure the buyer can afford the item
    if buyer.wallet >= credits:

        # the seller is the current item owner
        seller = item.owner

        # swap credits
        buyer.wallet -= credits
        seller.wallet += credits

        # take the item off the market
        item.is_for_sale = False

        # buyer gets the item
        item.owner = buyer

        # save all the changes
        item.save()
        buyer.save()
        seller.save()

        return True

    # buyer can't afford the item
    else:
        return False


def get_user_character(user):
    try:
        character = models.Character.objects.get(user=user)
    except ObjectDoesNotExist:
        character = None
    return character