import django
from django.test import TestCase

from toolkit.models import User
from toolkit.views.create_account import create_user

django.setup()


class Account_Creation_Tests(TestCase):
    """Unit tests for account creation page"""

    def test_create_user_positive(self):
        """Tests if the create user function successfully creates a new user"""
        create_user("test", "test@test.test", "test")
        check = User.objects.filter(username="test")
        self.assertTrue(check.exists)
        self.assertEqual(check[0].email, "test@test.test")
        self.assertTrue(check[0].check_password("test"))

    def test_create_user_negative(self):
        """Tests if the create user function does not create a new user"""
        temp = User(username="test2", password="test2", email="Test2@Test2.Test2")
        temp.save()
        with self.assertRaises(ValueError):
            create_user("test2", "test2@test2.test2", "test2")
