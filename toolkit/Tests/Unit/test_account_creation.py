from django.test import TestCase, Client
from django.urls import reverse
from toolkit.models import User


class TestCreateAccount(TestCase):
    """
    Testing for login page.
    """

    def setUp(self):
        """
        Function to set up all tests with information needed within
        each individual test case.
        """
        self.client = Client()
        self.create_account_url = reverse("create_account")
        self.home_url = "/"
        self.login_url = reverse("login")
        self.username = "dummy"
        self.email = "dummy@email.com"
        self.password = "dummy_password"
        self.test_user = User.objects.create_user(
            username=self.username, email=self.email, password=self.password
        )
        # self.save()

    def test_can_access_login_page(self):
        """
        Tests to see if a user is able to access the create account page.
        """
        response = self.client.get(self.create_account_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "create_account.html")

    def test_successful_login(self):
        """
        Tests if a user is able to login successfully after giving correct credentials
        """
        response = self.client.post(
            self.create_account_url,
            username=self.username,
            email=self.email,
            password=self.password,
        )
        self.assertEqual(response.status_code, 302)
        user = User.objects.filter(username=self.username).first()
        self.assertEqual(user, self.test_user)
        # response = self.client.login(username=self.username, password=self.password)
        # self.assertTrue(response)

    def test_unsuccessful_login_no_username(self):
        """
        Tests if a user is able to login after giving no username
        """
        response = self.client.post(
            self.create_account_url,
            {"username": "", "password": self.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.create_account_url)

    def test_unsuccessful_login_no_password(self):
        """
        Tests if a user is able to login after giving no password
        """
        response = self.client.post(
            self.create_account_url,
            {"username": self.username, "password": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.create_account_url)

    def test_unsuccessful_login_no_username_password(self):
        """
        Tests if a user is able to login after giving no username or password
        """
        response = self.client.post(
            self.create_account_url, {"username": "", "password": ""}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.create_account_url)

    def test_unsuccessful_login_wrong_username(self):
        """
        Tests if a user is able to login after giving incorrect username
        """
        response = self.client.post(
            self.create_account_url,
            {"username": "failure", "password": self.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.create_account_url)

    def test_unsuccessful_login_wrong_password(self):
        """
        Tests if a user is able to login after giving incorrect password
        """
        response = self.client.post(
            self.create_account_url,
            {"username": self.username, "password": "failure"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.create_account_url)
