from django.test import Client, TestCase
from django.contrib.auth.models import User

from model_mommy import mommy

from . import forms
from . import models


class CharacterTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.character = mommy.make(
            models.Character,
            user=self.users[0],
        )

    def test_character_exists(self):
        characters = models.Character.objects.all()
        self.assertIn(self.character, characters)

    def test_character_form(self):
        form = forms.CharacterForm({
            'name': self.character.name,
        })
        self.assertTrue(form.is_valid())

        character = form.save(commit=False)
        character.user = self.users[0]
        character.save()
        self.assertEqual(character.name, self.character.name)
        self.assertEqual(character.user, self.users[0])

    def test_character_form_blank(self):
        form = forms.CharacterForm({})
        self.assertFalse(form.is_valid())

    def test_character_detail(self):
        self.client.force_login(self.users[1])
        response = self.client.get('/characters/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "create character")

        data = {
            'name': 'brand new character',
        }
        response = self.client.post('/characters/create/', data)
        self.assertRedirects(response, '/characters/', 302, 200)
        response = self.client.get('/characters/')
        self.assertContains(response, data['name'])

    def test_character_edit(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/{}/edit/'.format(self.character.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.character.name)

        data = {
            'name': 'new character name',
        }
        response = self.client.post('/characters/{}/edit/'.format(self.character.pk), data)
        self.assertRedirects(response, '/characters/', 302, 200)
        response = self.client.get('/characters/')
        self.assertContains(response, data['name'])

    def test_character_delete(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/characters/{}/delete/'.format(self.character.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.character.name)

        response = self.client.post('/characters/{}/delete/'.format(self.character.pk))
        self.assertRedirects(response, '/characters/', 302, 200)

        characters = models.Character.objects.all()
        self.assertNotIn(self.character, characters)