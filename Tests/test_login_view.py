from django.contrib.auth import authenticate
from django.test import Client, TestCase
from django.urls import reverse

from toolkit.models import User


class TestLogin(TestCase):
    """Testing for login page."""

    def setUp(self):
        """
        Function to set up all tests with information needed within
        each individual test case.
        """
        self.client = Client()
        self.login_url = reverse("login")
        self.home_url = "/"
        self.create_account_url = reverse("create_account")
        self.username = "dummy"
        self.password = "password"
        self.test_user = User.objects.create(username=self.username)
        self.test_user.set_password(self.password)
        self.test_user.save()

    def tearDown(self):
        """Function to clean up test database after each individual test."""
        self.test_user.delete()

    def test_can_access_login_page(self):
        """Tests to see if a user is able to access the login page."""
        response = self.client.get(self.login_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_successful_login(self):
        """Tests if a user is able to login successfully after giving correct credentials."""
        user = authenticate(username=self.username, password=self.password)
        self.assertTrue((user is not None) and user.is_authenticated)
        response = self.client.post(
            self.login_url,
            data={"username": self.username, "password": self.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.home_url)

    def test_unsuccessful_login_no_username(self):
        """Tests if a user is able to login after giving no username."""
        user = authenticate(username="", password=self.password)
        self.assertFalse((user is not None) and user.is_authenticated)
        response = self.client.post(
            self.login_url,
            data={"username": "", "password": self.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)

    def test_unsuccessful_login_no_password(self):
        """Tests if a user is able to login after giving no password."""
        user = authenticate(username=self.username, password="")
        self.assertFalse((user is not None) and user.is_authenticated)
        response = self.client.post(
            self.login_url,
            data={"username": self.username, "password": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)

    def test_unsuccessful_login_no_username_password(self):
        """Tests if a user is able to login after giving no username or password."""
        user = authenticate(username="", password="")
        self.assertFalse((user is not None) and user.is_authenticated)
        response = self.client.post(
            self.login_url, data={"username": "", "password": ""}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)

    def test_unsuccessful_login_wrong_username(self):
        """Tests if a user is able to login after giving incorrect username."""
        user = authenticate(username="wrong", password=self.password)
        self.assertFalse((user is not None) and user.is_authenticated)
        response = self.client.post(
            self.login_url,
            data={"username": "wrong", "password": self.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)

    def test_unsuccessful_login_wrong_password(self):
        """Tests if a user is able to login after giving incorrect password."""
        user = authenticate(username=self.username, password="wrong")
        self.assertFalse((user is not None) and user.is_authenticated)
        response = self.client.post(
            self.login_url,
            data={"username": self.username, "password": "wrong"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)

    def test_can_access_login_page_filled_username(self):
        """Tests to see if a user is able to access the login page given the username as context."""
        response = self.client.get(
            self.login_url, data={"username": self.username}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")
