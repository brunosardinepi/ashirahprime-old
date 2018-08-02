from django.test import Client, TestCase
from django.contrib.auth.models import User

from model_mommy import mommy

from . import models
from characters.models import Character


class ItemTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)
        self.character = mommy.make(Character, user=self.users[0])
        self.character2 = mommy.make(Character, user=self.users[1], wallet=1000)
        self.items = mommy.make(models.Item, owner=self.character, _quantity=3)
        self.items += mommy.make(models.Item, owner=self.character2, _quantity=3)

    def test_item_exists(self):
        items = models.Item.objects.all()
        self.assertIn(self.items[0], items)
        self.assertIn(self.items[1], items)
        self.assertIn(self.items[2], items)
        self.assertIn(self.items[3], items)
        self.assertIn(self.items[4], items)
        self.assertIn(self.items[5], items)

    def test_item_list(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.items[0].name)
        self.assertContains(response, self.items[1].name)
        self.assertContains(response, self.items[2].name)
        self.assertNotContains(response, self.items[3].name)
        self.assertNotContains(response, self.items[4].name)
        self.assertNotContains(response, self.items[5].name)
        self.client.logout()

        self.client.force_login(self.users[1])
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.items[0].name)
        self.assertNotContains(response, self.items[1].name)
        self.assertNotContains(response, self.items[2].name)
        self.assertContains(response, self.items[3].name)
        self.assertContains(response, self.items[4].name)
        self.assertContains(response, self.items[5].name)

    def test_item_detail(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/items/{}/'.format(self.items[0].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.items[0].name)

    def test_equip_item(self):
        self.assertEqual(self.character.armor, None)
        self.assertEqual(self.character.weapon, None)

        self.client.force_login(self.users[0])
        response = self.client.get('/items/{}/equip/'.format(self.items[0].pk))
        self.assertRedirects(response, '/characters/', 302, 200)
        response = self.client.get('/characters/')
        self.assertContains(response, self.items[0])

    def test_unequip_item(self):
        self.character.armor = self.items[0]
        self.character.save()

        self.assertEqual(self.character.armor, self.items[0])

        self.client.force_login(self.users[0])
        response = self.client.get('/items/{}/unequip/'.format(self.items[0].pk))
        self.assertRedirects(response, '/characters/', 302, 200)
        response = self.client.get('/characters/')
        self.assertNotContains(response, self.items[0])

    def test_sell_items(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/items/sell/')
        self.assertEqual(response.status_code, 200)

        # make sure the sell list has the right items for this user only
        self.assertContains(response, self.items[0].name)
        self.assertContains(response, self.items[1].name)
        self.assertContains(response, self.items[2].name)
        self.assertNotContains(response, self.items[3].name)
        self.assertNotContains(response, self.items[4].name)
        self.assertNotContains(response, self.items[5].name)

        # formset data
        data = {
            'item_set-INITIAL_FORMS': '3',
            'item_set-TOTAL_FORMS': '3',
            'item_set-MIN_NUM_FORMS': '0',
            'item_set-MAX_NUM_FORMS': '1000',
            'item_set-0-id': self.items[0].pk,
            'item_set-0-name': self.items[0].name,
            'item_set-0-is_for_sale': 'checked',
            'item_set-0-sale_price': '100',
            'item_set-1-id': self.items[1].pk,
            'item_set-1-name': self.items[1].name,
            'item_set-1-is_for_sale': 'checked',
            'item_set-1-sale_price': '200',
            'item_set-2-id': self.items[2].pk,
            'item_set-2-name': self.items[2].name,
            'item_set-2-is_for_sale': 'checked',
            'item_set-2-sale_price': '300',
        }

        # post data, redirect to the same page
        response = self.client.post('/items/sell/', data=data)
        self.assertRedirects(response, '/items/sell/', 302, 200)
        response = self.client.get('/items/sell/')
        self.assertEqual(response.status_code, 200)

        # sell list reflects the new price
        self.assertContains(response, self.items[0].name)
        self.assertContains(response, self.items[0].sale_price)

    def test_buy_item(self):
        # set initial data
        item = self.items[0]
        item.is_for_sale = True
        item.sale_price = 600
        item.save()

        character = self.character2

        # check for items on market list
        self.items[3].is_for_sale = True
        self.items[3].save()

        self.client.force_login(self.users[1])
        response = self.client.get('/items/market/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item.name)
        self.assertContains(response, item.sale_price)
        self.assertContains(response, "buy")
        # shouldn't see this item because it's not for sale
        self.assertNotContains(response, self.items[1].name)
        # shouldn't see this item because it's mine
        self.assertNotContains(response, self.items[3].name)

        # buy item confirmation page
        response = self.client.get('/items/{}/buy/'.format(item.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item.name)
        self.assertContains(response, item.sale_price)

        # form data
        data = {'name': item.name}

        # post data
        response = self.client.post('/items/{}/buy/'.format(item.pk), data=data)
        self.assertRedirects(response, '/items/', 302, 200)

        # check for new item in list
        response = self.client.get('/items/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, item.name)

        # check wallet amount
        response = self.client.get('/items/sell/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "wallet: {}".format(
            character.wallet - item.sale_price))

        # other user shouldn't have item in inventory
        self.client.force_login(self.users[0])
        response = self.client.get('/items/')
        self.assertNotContains(response, item.name)
