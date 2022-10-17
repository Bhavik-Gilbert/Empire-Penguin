"""Tests of the login view"""
from django.contrib import messages
from django.test import TestCase
from django.urls import reverse


from microblogs.models import User
from microblogs.forms import LogInForm
from .helpers import LogInTester

class LogInViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('login')
        self.user = User.objects.create_user(
            first_name ='Jane',
            last_name ='Doe',
            username = '@janedoe',
            email = 'janedoe@example.org',
            bio ='hi',
            password = 'Password123',
            is_active = True
        )

    def test_login_url(self):
        self.assertEqual(self.url, '/login/')

    def test_get_login(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_login(self):
        form_input = {'username': '@johndoe', 'password': 'WRONGPASSWORD'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        message = list(response.context['messages'])
        self.assertEqual(1, len(message))
        self.assertEqual(message[0].level, messages.ERROR)
    
    def test_login_with_blank_username(self):
        form_input = {'username': '', 'password': 'Password123'}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        message = list(response.context['messages'])
        self.assertEqual(1, len(message))
        self.assertEqual(message[0].level, messages.ERROR)
    
    def test_login_with_blank_password(self):
        form_input = {'username': '@johndoe', 'password': ''}
        response = self.client.post(self.url, form_input)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        message = list(response.context['messages'])
        self.assertEqual(1, len(message))
        self.assertEqual(message[0].level, messages.ERROR)

    def test_successul_login(self):
        form_input = {'username': '@janedoe', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertTrue(self._is_logged_in())
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        message = list(response.context['messages'])
        self.assertEqual(0, len(message))

    def test_valid_login_by_inactive_user(self):
        self.user.is_active = False
        self.user.save()
        form_input = {'username': '@janedoe', 'password': 'Password123'}
        response = self.client.post(self.url, form_input, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'login.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, LogInForm))
        self.assertFalse(form.is_bound)
        self.assertFalse(self._is_logged_in())
        message = list(response.context['messages'])
        self.assertEqual(1, len(message))
        self.assertEqual(message[0].level, messages.ERROR)