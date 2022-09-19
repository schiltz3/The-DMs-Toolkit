from django.shortcuts import redirect, render
from django.views import View

from ..models import Account


class Login(View):
    """
    A class to handle the login page's GET and POST requests. As well as retrieve
    a user's credentials from the Account database.
    """

    @staticmethod
    def get(self, request):
        """
        GET method for login page.
        """
        return render(request, "login.html")

    @staticmethod
    def post(self, request):
        """
        POST method for login page.
        """
        return render(request, "login.html")

    def retrieve_user(self):
        """
        Function used to retrieve the credentials of a user and validate them or not.
        """
        pass  # Function to be implemented in separate PR
