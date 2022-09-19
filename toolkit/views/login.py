from django.shortcuts import render
from django.views import View


class Login(View):
    """
    A class to handle the login page's GET and POST requests. As well as retrieve
    a user's credentials from the Account database.
    """
    @staticmethod
    def get(self, request):
        """GET method for login page."""
        return render(request, "login.html")

    @staticmethod
    def post(self, request):
        """POST method for login page."""
        return render(request, "login.html")