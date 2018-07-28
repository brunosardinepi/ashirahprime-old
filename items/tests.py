from django.test import Client, TestCase
from django.contrib.auth.models import User

from model_mommy import mommy

from . import models


class ItemTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.items = mommy.make(models.Item, user=self.users[0], _quantity=3)
        self.items += mommy.make(models.Item, user=self.users[1], _quantity=3)

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