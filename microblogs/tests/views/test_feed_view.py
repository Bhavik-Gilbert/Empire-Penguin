"""Tests of the feed view."""
from django.test import TestCase
from django.urls import reverse

from microblogs.forms import PostForm
from microblogs.models import User
from microblogs.tests.helpers import reverse_with_next


class FeedViewTestCase(TestCase):
    """Tests of the feed view."""

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('feed')
        self.user = User.objects.get(username="janedoe")

    def test_feed_url(self):
        self.assertEqual(self.url, '/feed/')

    def test_get_feed(self):
        self.client.login(username=self.user.username, password="Password123")
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'feed.html')

    def test_get_feed_with_redirect_when_not_logged_in(self):
        redirect_url = reverse_with_next('login', self.url)
        response = self.client.get(self.url)
        self.assertRedirects(
            response,
            redirect_url,
            status_code=302,
            target_status_code=200)
