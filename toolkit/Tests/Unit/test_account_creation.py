from django.test import TestCase, Client
from django.urls import reverse
from toolkit.models import User


class TestLogin(TestCase):
    """
    Testing for login page.
    """

    def setUp(self):
        """
        Function to set up all tests with information needed within
        each individual test case.
        """
        self.client = Client()
        self.login_url = reverse("login")
        self.home_url = "/"
        self.create_account_url = reverse("create_account")
        self.test_user = User.objects.create_user(
            username="dummy", email="dummy@uwm.edu", password="password"
        )
        self.test_user.save()

    def test_can_access_login_page(self):
        """
        Tests to see if a user is able to access the login page.
        """
        response = self.client.get(self.login_url)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "login.html")

    def test_successful_login(self):
        """
        Tests if a user is able to login successfully after giving correct credentials
        """
        user = User.objects.filter(username=self.test_user.username).first()
        user.is_active = True
        user.save()
        response = self.client.post(
            self.login_url,
            username=self.test_user.username,
            password=self.test_user.password,
        )
        self.assertEqual(response.status_code, 302)
        # response = self.client.login(username=self.test_user.username, password=self.test_user.password)
        # self.assertTrue(response)

    def test_unsuccessful_login_no_username(self):
        """
        Tests if a user is able to login after giving no username
        """
        response = self.client.post(
            self.login_url,
            {"username": "", "password": self.test_user.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)

    def test_unsuccessful_login_no_password(self):
        """
        Tests if a user is able to login after giving no password
        """
        response = self.client.post(
            self.login_url,
            {"username": self.test_user.username, "password": ""},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)

    def test_unsuccessful_login_no_username_password(self):
        """
        Tests if a user is able to login after giving no username or password
        """
        response = self.client.post(
            self.login_url, {"username": "", "password": ""}, follow=True
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)

    def test_unsuccessful_login_wrong_username(self):
        """
        Tests if a user is able to login after giving incorrect username
        """
        response = self.client.post(
            self.login_url,
            {"username": "failure", "password": self.test_user.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)

    def test_unsuccessful_login_wrong_password(self):
        """
        Tests if a user is able to login after giving incorrect password
        """
        response = self.client.post(
            self.login_url,
            {"username": self.test_user.username, "password": "failure"},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertRedirects(response, self.login_url)
