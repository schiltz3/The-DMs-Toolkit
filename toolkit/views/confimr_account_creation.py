from django.shortcuts import render
from django.views import View
from django.http.request import HttpRequest


class ConfirmAccountCreation(View):
    """
    A class to handle the confirm account creation page's GET and POST requests.
    """

    def get(self, request: HttpRequest):
        """GET method for confirm account creation page."""
        return render(request, "confirm_account_creation.html")

    def post(self, request: HttpRequest):
        """POST method for confirm account creation page."""
        return render(request, "confirm_account_creation.html")
