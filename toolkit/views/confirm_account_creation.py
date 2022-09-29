from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views import View


class ConfirmAccountCreation(View):
    """A class to handle the confirm account creation page's GET and POST requests."""

    @staticmethod
    def get(request: HttpRequest, **kwargs):
        """GET method for confirm account creation page.
        Args:
            request (HttpRequest):
            kwargs (dict[str, str]): username
        """
        return render(request, "confirm_account_creation.html")

    @staticmethod
    def post(request: HttpRequest, **kwargs):
        """POST method for confirm account creation page."""
        username = kwargs.get("username", "")
        return redirect(
            "login",
            username=username,
            permanent=True,
        )
