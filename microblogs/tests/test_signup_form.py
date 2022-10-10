"""  Unit tests for Signup Form """
from django.test import TestCase
from django import forms

from microblogs.forms import SignUpForm
from microblogs.models import User

# Create your tests here.
class SignUpFormTesCase(TestCase):
    def setUp(self):
        self.form_input = {
            'first_name':'Jane',
            'last_name':'Doe',
            'username':'@janedoe',
            'email':'janedoe@example.org',
            'bio':'hi',
            'new_password':'Password123',
            'password_confirmation':'Password123'
        }

    def test_valid_signup_form(self):
        form = SignUpForm(data=self.form_input)
        self.assertTrue(form.is_valid())

    def test_form_has_necessary_fields(self):
        form = SignUpForm()
        self.assertIn('first_name', form.fields)
        self.assertIn('last_name', form.fields)
        self.assertIn('username', form.fields)
        self.assertIn('email', form.fields)
        email_field = form.fields['email']
        self.assertTrue(isinstance(email_field, forms.EmailField))
        self.assertIn('bio', form.fields)
        self.assertIn('new_password', form.fields)
        new_password_widget = form.fields['new_password'].widget
        self.assertTrue(isinstance(new_password_widget, forms.PasswordInput))
        self.assertIn('password_confirmation', form.fields)
        password_confirmation_widget = form.fields['password_confirmation'].widget
        self.assertTrue(isinstance(password_confirmation_widget, forms.PasswordInput))

    def test_form_uses_valid_model(self):
        self.form_input['username'] = 'badusername'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    
    def test_password_must_contain_uppercase_character(self):
        self.form_input['new_password'] = 'password123'
        self.form_input['password_confirmation'] = 'password123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_lowercase_character(self):
        self.form_input['new_password'] = 'PASSWORD123'
        self.form_input['password_confirmation'] = 'PASSWORD123'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())

    def test_password_must_contain_number(self):
        self.form_input['new_password'] = 'Passwordabc'
        self.form_input['password_confirmation'] = 'Passwordabc'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())
    

    #New password and password confirmation must be identical
    def test_new_pasword_and_password_confirmation_identical(self):
        self.form_input['new_password'] = 'Password123'
        self.form_input['password_confirmation'] = 'Password12'
        form = SignUpForm(data=self.form_input)
        self.assertFalse(form.is_valid())