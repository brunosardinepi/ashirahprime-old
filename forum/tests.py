from django.test import Client, TestCase
from django.contrib.auth.models import User

from model_mommy import mommy

from . import models


class ForumTest(TestCase):
    def setUp(self):
        self.client = Client()

        self.users = mommy.make(User, _quantity=2)

        self.forums = mommy.make(models.Forum, _quantity=2)

        self.post = mommy.make(
            models.Post,
            user=self.users[0],
            forum=self.forums[0],
        )

        self.post2 = mommy.make(
            models.Post,
            user=self.users[1],
            forum=self.forums[1],
        )

        self.comment = mommy.make(
            models.Comment,
            user=self.users[1],
            post=self.post,
        )

        self.comment2 = mommy.make(
            models.Comment,
            user=self.users[0],
            post=self.post2,
        )

    def test_forum_exists(self):
        forums = models.Forum.objects.all()
        self.assertIn(self.forums[0], forums)
        self.assertIn(self.forums[1], forums)

    def test_post_exists(self):
        posts = models.Post.objects.all()
        self.assertIn(self.post, posts)
        self.assertIn(self.post2, posts)

    def test_comment_exists(self):
        comments = models.Comment.objects.all()
        self.assertIn(self.comment, comments)
        self.assertIn(self.comment2, comments)

    def test_forum_page(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/forum/')
        self.assertEqual(response.status_code, 200)

        # forum list should contain the forum names
        self.assertContains(response, self.forums[0].name)
        self.assertContains(response, self.forums[1].name)

    def test_forum_detail(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/forum/{}/'.format(self.forums[0].pk))
        self.assertEqual(response.status_code, 200)

        # specific forum page should contain the forum name
        # and its posts
        # but not posts from another forum or other forum names
        self.assertContains(response, self.forums[0].name)
        self.assertContains(response, self.post.title)
        self.assertNotContains(response, self.forums[1].name)
        self.assertNotContains(response, self.post2.title)

    def test_post_detail(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/forum/{}/post/{}/'.format(
            self.forums[0].pk, self.post.pk))
        self.assertEqual(response.status_code, 200)

        # specific post should contain the post title
        # and its comments
        # but not other post titles or other comments
        self.assertContains(response, self.post.title)
        self.assertContains(response, self.comment.body)
        self.assertNotContains(response, self.post2.title)
        self.assertNotContains(response, self.comment2.body)

    def test_post_create(self):
        self.client.force_login(self.users[0])
        response = self.client.get('/forum/{}/post/create/'.format(self.forums[0].pk))
        self.assertEqual(response.status_code, 200)

        # create a new post
        title = 'my new post title'
        body = 'hello ashirah prime'
        data = {
            'title': title,
            'body': body,
        }
        response = self.client.post(
            '/forum/{}/post/create/'.format(self.forums[0].pk),
            data=data,
        )

        # get the post pk to reference in the url
        post = models.Post.objects.get(title=title)
        self.assertRedirects(response,
            '/forum/{}/post/{}/'.format(self.forums[0].pk, post.pk),
            302, 200)

        # check if the post title and body are on the page
        response = self.client.get(
            '/forum/{}/post/{}/'.format(self.forums[0].pk, post.pk))
        self.assertContains(response, title)
        self.assertContains(response, body)

    def test_comment_create(self):
        self.client.force_login(self.users[1])
        response = self.client.get(
            '/forum/{}/post/{}/comment/create/'.format(
            self.forums[0].pk, self.post.pk))
        self.assertEqual(response.status_code, 200)

        # create a new comment
        body = 'i am a human and not a robot'
        data = {'body': body}
        response = self.client.post(
            '/forum/{}/post/{}/comment/create/'.format(
            self.forums[0].pk, self.post.pk),
            data=data,
        )
        self.assertRedirects(response,
            '/forum/{}/post/{}/'.format(self.forums[0].pk, self.post.pk),
            302, 200)

        # check if the comment is on the page
        response = self.client.get(
            '/forum/{}/post/{}/'.format(self.forums[0].pk, self.post.pk))
        self.assertContains(response, body)
