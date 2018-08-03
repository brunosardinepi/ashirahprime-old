from django.test import Client, TestCase
from django.contrib.auth.models import User

from model_mommy import mommy

from . import models
from characters.models import Character


class GuildTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)
        self.character = mommy.make(Character, user=self.users[0])
        self.character2 = mommy.make(Character, user=self.users[1])
        self.guild = mommy.make(models.Guild, creator=self.character)
        self.guild2 = mommy.make(models.Guild, creator=self.character2, is_public=False)
        self.guild.members.add(self.character)
        self.guild2.members.add(self.character2)

    def test_guild_exists(self):
        guilds = models.Guild.objects.all()
        self.assertIn(self.guild, guilds)
        self.assertIn(self.guild2, guilds)

    def test_guild_list(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/guilds/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.guild.name)
        self.client.logout()

        self.client.force_login(self.users[1])
        response = self.client.get('/guilds/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.guild2.name)

    def test_guild_detail(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/guilds/{}/'.format(self.guild.pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.guild.name)
        self.assertContains(response, self.character.name)

    def test_guild_search(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/guilds/search/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.guild.name)
        self.assertNotContains(response, self.guild2.name)

    def test_guild_create(self):
        # login and go to guild create page
        self.client.force_login(self.users[0])
        response = self.client.get('/guilds/create/')
        self.assertEqual(response.status_code, 200)

        # form data
        new_guild_name = 'my cool new guild'
        data = {
            'name': new_guild_name,
            'is_public': True,
        }

        # submit guild create form
        response = self.client.post('/guilds/create/', data=data)
        # check the redirect
        self.assertRedirects(response, '/guilds/', 302, 200)
        # make sure the new guild shows up in our guild list
        response = self.client.get('/guilds/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_guild_name)

        # make sure the new guild shows up in the guild search list
        response = self.client.get('/guilds/search/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_guild_name)

        # create a private guild
        new_guild_name = 'super secret guild'
        data = {
            'name': new_guild_name,
            'is_public': False,
        }
        response = self.client.post('/guilds/create/', data=data)
        # check for the guild in the guild search list
        self.client.logout()
        self.client.force_login(self.users[1])
        response = self.client.get('/guilds/search/')
        self.assertNotContains(response, new_guild_name)

    def test_guild_edit(self):
        # login and go to guild edit page
        self.client.force_login(self.users[0])
        response = self.client.get('/guilds/{}/edit/'.format(self.guild.pk))
        self.assertEqual(response.status_code, 200)

        # form data
        new_guild_name = 'i changed the name'
        data = {
            'name': new_guild_name,
            'is_public': True,
        }

        # submit guild edit form
        response = self.client.post('/guilds/{}/edit/'.format(self.guild.pk), data=data)
        # check the redirect
        self.assertRedirects(response, '/guilds/', 302, 200)
        # make sure the guild name change shows up in our guild list
        response = self.client.get('/guilds/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_guild_name)

        # make sure the guild change shows up in the guild search list
        response = self.client.get('/guilds/search/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, new_guild_name)

        # change the guild to private
        data = {
            'name': new_guild_name,
            'is_public': False,
        }
        response = self.client.post('/guilds/{}/edit/'.format(self.guild.pk), data=data)
        # check for the guild in the guild search list
        self.client.logout()
        self.client.force_login(self.users[1])
        response = self.client.get('/guilds/search/')
        self.assertNotContains(response, new_guild_name)

    def test_join_guild(self):
        # login and go to guild join page
        self.client.force_login(self.users[0])
        response = self.client.get('/guilds/{}/join/'.format(self.guild2.pk))
        self.assertEqual(response.status_code, 200)

        # form data
        data = {
            'name': self.guild2.name,
            'is_public': self.guild2.is_public,
        }

        # submit guild join form
        response = self.client.post('/guilds/{}/join/'.format(self.guild2.pk), data=data)
        # check the redirect
        self.assertRedirects(response, '/guilds/', 302, 200)
        # make sure the guild shows up in our guild list
        response = self.client.get('/guilds/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.guild2.name)

    def test_leave_guild(self):
        # login and go to guild leave page
        self.client.force_login(self.users[0])
        response = self.client.get('/guilds/{}/leave/'.format(self.guild.pk))
        self.assertEqual(response.status_code, 200)

        # form data
        data = {
            'name': self.guild.name,
            'is_public': self.guild.is_public,
        }

        # submit guild leave form
        response = self.client.post('/guilds/{}/leave/'.format(self.guild.pk), data=data)
        # check the redirect
        self.assertRedirects(response, '/guilds/', 302, 200)
        # make sure the guild doesn't show up in our guild list
        response = self.client.get('/guilds/')
        self.assertEqual(response.status_code, 200)
        self.assertNotContains(response, self.guild.name)
