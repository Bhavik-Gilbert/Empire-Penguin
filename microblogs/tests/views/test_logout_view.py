"""Tests of the log out view"""
from urllib import response
from django.test import TestCase
from django.urls import reverse

from microblogs.models import User
from ..helpers import LogInTester


class LogOutViewTestCase(TestCase, LogInTester):

    fixtures = ['microblogs/tests/fixtures/default_user.json']

    def setUp(self):
        self.url = reverse('logout')
        self.user = User.objects.get(username="janedoe")

    def test_logout_url(self):
        self.assertEqual(self.url, '/logout/')

    def test_get_logout(self):
        self.client.login(username='janedoe', password='Password123')
        self.assertTrue(self._is_logged_in())
        response = self.client.get(self.url, follow=True)
        response_url = reverse('home')
        self.assertRedirects(
            response,
            response_url,
            status_code=302,
            target_status_code=200)
        self.assertTemplateUsed(response, 'home.html')
        self.assertFalse(self._is_logged_in())
