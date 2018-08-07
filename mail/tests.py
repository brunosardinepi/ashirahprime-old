from django.test import Client, TestCase
from django.contrib.auth.models import User

from model_mommy import mommy

from . import models
from characters.models import Character


class MailTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)
        self.character = mommy.make(Character, user=self.users[0])
        self.character2 = mommy.make(Character, user=self.users[1])
        self.messages = mommy.make(
            models.Message,
            sender=self.character,
            recipient=self.character2,
            _quantity=3,
        )
        self.messages += mommy.make(
            models.Message,
            sender=self.character2,
            recipient=self.character,
            _quantity=3,
        )

    def test_message_exists(self):
        messages = models.Message.objects.all()
        self.assertIn(self.messages[0], messages)
        self.assertIn(self.messages[1], messages)
        self.assertIn(self.messages[2], messages)
        self.assertIn(self.messages[3], messages)
        self.assertIn(self.messages[4], messages)
        self.assertIn(self.messages[5], messages)

    def test_message_list(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/mail/')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.messages[0].sender.name)
        self.assertContains(response, self.messages[0].recipient.name)
        self.assertContains(response, self.messages[0].subject)
        self.assertContains(response, self.messages[3].sender.name)
        self.assertContains(response, self.messages[3].recipient.name)
        self.assertContains(response, self.messages[3].subject)

    def test_message_detail(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/mail/{}/'.format(self.messages[3].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.messages[3].sender.name)
        self.assertContains(response, self.messages[3].recipient.name)
        self.assertContains(response, self.messages[3].subject)
        self.assertContains(response, self.messages[3].body)
        self.assertContains(response, "reply")

        # "reply" shouldn't be on a message we sent
        response = self.client.get('/mail/{}/'.format(self.messages[0].pk))
        self.assertNotContains(response, "reply")

    def test_message_reply(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/mail/{}/reply/'.format(self.messages[3].pk))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.messages[3].sender.name)
        self.assertContains(response, self.messages[3].subject)

    def test_message_send(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/mail/create/')
        self.assertEqual(response.status_code, 200)

        # send the mail
        subject = 'this is a test subject'
        body = 'hello friend pls respond'
        data = {
            'recipient': self.users[1].pk,
            'subject': subject,
            'body': body,
        }
        response = self.client.post('/mail/create/', data=data)
        self.assertRedirects(response, '/mail/', 302, 200)

        # make sure mail is in sent folder
        response = self.client.get('/mail/')
        self.assertContains(response, subject)
        self.client.logout()

        # make sure mail is in users[1] inbox
        self.client.force_login(self.users[1])
        response = self.client.get('/mail/')
        self.assertContains(response, subject)

    def test_message_read(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/mail/')
        self.assertEqual(response.status_code, 200)

        # check if messages are 'unread'
        self.assertContains(response, 'unread', count=3)

        # 'read' the messages
        self.client.get('/mail/{}/'.format(self.messages[3].pk))
        self.client.get('/mail/{}/'.format(self.messages[4].pk))
        self.client.get('/mail/{}/'.format(self.messages[5].pk))

        # check if the messages are now 'read'
        response = self.client.get('/mail/')
        self.assertNotContains(response, 'unread')
        self.assertContains(response, 'read', count=3)
