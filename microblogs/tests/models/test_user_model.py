""" Unit tests for User Model """

from django.test import TestCase
from django.core.exceptions import ValidationError

from microblogs.models import User

# Create your tests here.
class UserModelTestCase(TestCase):
    fixtures = [
        'microblogs/tests/fixtures/default_user.json',
        'microblogs/tests/fixtures/other_users.json'
    ]

    # Setup code run before every test
    def setUp(self):
        self.user = User.objects.get(username="@janedoe")


    def test_valid_user(self):
        self._assert_user_is_valid()

    def test_username_cannot_be_blank(self):
        self.user.username = ''
        self._assert_user_is_invalid()
    
    def test_username_can_be_30_characters_long(self):
        self.user.username = '@' + 'x' * 29
        self._assert_user_is_valid()

    def test_username_cannot_be_over_30_characters_long(self):
        self.user.username = '@' + 'x' * 30
        self._assert_user_is_invalid()

    def test_username_must_be_unqiue(self):
        user = User.objects.get(username="@johndoe")
        self.user.username = '@johndoe'
        self._assert_user_is_invalid()
    
    def test_username_must_start_with_at_symbol(self):
        self.user.username = 'johndoe'
        self._assert_user_is_invalid()

    def test_username_must_conatin_only_alphanumericals_after_at(self):
        self.user.username = '@john!doe'
        self._assert_user_is_invalid()
    
    def test_username_must_conatin_atleast_3_alphanumericals_after_at(self):
        self.user.username = '@jo'
        self._assert_user_is_invalid()
    
    def test_username_may_contain_numbers(self):
        self.user.username = '@j0hndoe2'
        self._assert_user_is_valid()
    
    def test_username_must_contain_only_one_at(self):
        self.user.username = '@johndoe@'
        self._assert_user_is_invalid()

    def test_firstname_must_not_be_blank(self):
        self.user.first_name = ''
        self._assert_user_is_invalid()

    def test_firstname_may_aleady_exist(self):
        user = User.objects.get(username="@johndoe")
        self.user.first_name = 'Jane'
        self._assert_user_is_valid()
    
    def test_firstname_can_be_50_characters_long(self):
        self.user.first_name = 'x' * 50
        self._assert_user_is_valid()

    def test_firstname_cannot_be_over_50_characters_long(self):
        self.user.first_name = 'x' * 51
        self._assert_user_is_invalid()
    
    def test_lastname_must_not_be_blank(self):
        self.user.last_name = ''
        self._assert_user_is_invalid()

    def test_lastname_may_aleady_exist(self):
        user = User.objects.get(username="@johndoe")
        self.user.last_name = 'Doe'
        self._assert_user_is_valid()
    
    def test_lastname_can_be_50_characters_long(self):
        self.user.last_name = 'x' * 50
        self._assert_user_is_valid()

    def test_lastname_cannot_be_over_50_characters_long(self):
        self.user.last_name = 'x' * 51
        self._assert_user_is_invalid()
    
    def test_email_must_be_unique(self):
        user = User.objects.get(username="@johndoe")
        self.user.email ='johndoe@example.org'
        self._assert_user_is_invalid()

    def test_email_cannot_be_blank(self):
        self.user.email=''
        self._assert_user_is_invalid()
    
    def test_email_must_have_at_in_the_middle(self):
        self.user.email='janedoe.com'
        self._assert_user_is_invalid()
    
    def test_email_must_have_dot_at_the_end(self):
        self.user.email='janedoe@exampleorg'
        self._assert_user_is_invalid()
    
    def test_bio_can_be_blank(self):
        self.user.bio=''
        self._assert_user_is_valid()

    def test_bio_may_already_exist(self):
        user = User.objects.get(username="@johndoe")
        self.user.bio='hi'
        self._assert_user_is_valid()
    
    def test_bio_can_be_520_characters_long(self):
        self.user.bio = 'x' * 520
        self._assert_user_is_valid()

    def test_bio_cannot_be_over_520_characters_long(self):
        self.user.bio = 'x' * 521
        self._assert_user_is_invalid()

    # Pass assertion
    def _assert_user_is_valid(self):
        try:
            self.user.full_clean()
        except (ValidationError):
            self.fail("Test user should be valid")

    # Fail assertion
    def _assert_user_is_invalid(self):
        with self.assertRaises(ValidationError):
            self.user.full_clean()