from django.test import Client, TestCase
from django.urls import reverse

from toolkit.views.create_account import CreateAccountForm


class TestCreateAccount(TestCase):
    """Testing for create account and confirm account creation page."""

    def setUp(self):
        """
        Function to set up all tests with information needed within
        each individual test case.
        """
        self.client = Client()
        self.login_url = reverse("login")
        self.login_username_url = "/login/dummy"
        self.home_url = "/"
        self.create_account_url = reverse("create_account")
        self.confirm_account_creation_url = (
            "/create_account/confirm_account_creation/dummy"
        )
        self.username = "dummy"
        self.password = "password"
        self.email = "dummy@uwm.edu"

    def test_can_access_create_account_page(self):
        """Tests to see if a user is able to access the create user page."""
        response = self.client.get(self.create_account_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_account.html")

    def test_form_valid(self):
        """Tests if the form is valid after giving correct credentials."""
        form = CreateAccountForm(
            data={
                "email": self.email,
                "username": self.username,
                "password": self.password,
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_email(self):
        """Tests if the form is valid after giving incorrect credentials."""
        form = CreateAccountForm(
            data={
                "email": "dummy",
                "username": self.username,
                "password": self.password,
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_no_email(self):
        """Tests if the form is valid after giving incorrect credentials."""
        form = CreateAccountForm(
            data={"email": "", "username": self.username, "password": self.password}
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_no_username(self):
        """Tests if the form is valid after giving incorrect credentials."""
        form = CreateAccountForm(
            data={"email": self.email, "username": "", "password": self.password}
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_no_password(self):
        """Tests if the form is valid after giving incorrect credentials."""
        form = CreateAccountForm(
            data={"email": self.email, "username": self.username, "password": ""}
        )
        self.assertFalse(form.is_valid())

    def test_successful_account_creation(self):
        """Tests if a user is able to successfully create a new account giving correct credentials"""
        response = self.client.post(
            self.create_account_url,
            data={
                "email": self.email,
                "username": self.username,
                "password": self.password,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(
            response, self.confirm_account_creation_url, status_code=301
        )

    def test_unsuccessful_account_creation_email(self):
        """Tests if a user is able to successfully create a new account giving incorrect credentials"""
        response = self.client.post(
            self.create_account_url,
            data={
                "email": "dummy",
                "username": self.username,
                "password": self.password,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])

    def test_unsuccessful_account_creation_no_email(self):
        """Tests if a user is able to successfully create a new account giving incorrect credentials"""
        response = self.client.post(
            self.create_account_url,
            data={"email": "", "username": self.username, "password": self.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])

    def test_unsuccessful_account_creation_no_username(self):
        """Tests if a user is able to successfully create a new account giving incorrect credentials"""
        response = self.client.post(
            self.create_account_url,
            data={"email": self.email, "username": "", "password": self.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])

    def test_unsuccessful_account_creation_no_password(self):
        """Tests if a user is able to successfully create a new account giving incorrect credentials"""
        response = self.client.post(
            self.create_account_url,
            data={"email": self.email, "username": self.username, "password": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.redirect_chain, [])

    def test_confirm_creation_redirect_login(self):
        """Tests if a user is able to redirect to the login page after confirming account creation"""
        response = self.client.post(self.confirm_account_creation_url, follow=True)
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_username_url, status_code=301)
