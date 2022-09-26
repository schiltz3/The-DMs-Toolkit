from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views import View


class ConfirmAccountCreation(View):
    """
    A class to handle the confirm account creation page's GET and POST requests.
    """

    def get(self, request: HttpRequest, **kwargs):
        """GET method for confirm account creation page."""
        email = kwargs.get("email", "")
        return render(request, "confirm_account_creation.html")

    def post(self, request: HttpRequest, **kwargs):
        """POST method for confirm account creation page."""
        email = kwargs.get("email", "")
        return redirect(
            "login",
            email=email,
            permanent=True,
        )
