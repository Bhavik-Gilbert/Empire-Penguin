"""Tests of the signup view"""
from audioop import reverse
from django.test import TestCase
from django.urls import reverse
from django.contrib.auth.hashers import check_password

from microblogs.models import User
from microblogs.forms import SignUpForm
from ..helpers import LogInTester

class SignupViewTestCase(TestCase, LogInTester):

    def setUp(self):
        self.url = reverse('signup')
        self.form_input = {
            'first_name':'Jane',
            'last_name':'Doe',
            'username':'@janedoe',
            'email':'janedoe@example.org',
            'bio':'hi',
            'new_password':'Password123',
            'password_confirmation':'Password123'
        }

    def test_signup_url(self):
        self.assertEqual(self.url, '/signup/')

    def test_get_signup(self):
        response = self.client.get(self.url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertFalse(form.is_bound)

    def test_unsuccessful_signup(self):
        self.form_input['username'] = 'BAD_USERNAME'
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input)
        after_count = User.objects.count()
        self.assertEqual(before_count, after_count)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, 'signup.html')
        form = response.context['form']
        self.assertTrue(isinstance(form, SignUpForm))
        self.assertTrue(form.is_bound)
        self.assertFalse(self._is_logged_in())
    
    def test_successful_signup(self):
        before_count = User.objects.count()
        response = self.client.post(self.url, self.form_input, follow=True)
        after_count = User.objects.count()
        self.assertEqual(before_count + 1, after_count)
        response_url = reverse('feed')
        self.assertRedirects(response, response_url, status_code=302, target_status_code=200)
        self.assertTemplateUsed(response, 'feed.html')
        user = User.objects.get(username='@janedoe')
        self.assertEqual(user.first_name, 'Jane')
        self.assertEqual(user.last_name, 'Doe')
        self.assertEqual(user.email, 'janedoe@example.org')
        self.assertEqual(user.bio, 'hi')
        is_password_correct = check_password('Password123', user.password)
        self.assertTrue(is_password_correct)
        self.assertTrue(self._is_logged_in())