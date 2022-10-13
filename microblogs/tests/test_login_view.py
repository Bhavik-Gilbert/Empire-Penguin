"""Tests of the login view"""
from audioop import reverse
from django.test import TestCase
from django.urls import reverse

from microblogs.forms import LogInForm

class LogInViewTestCase(TestCase):

    def setUp(self):
        self.url = reverse('login')

    def test_login_url(self):
        self.assertEqual(self.url, '/login/')

    def test_get_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)