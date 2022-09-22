from django.shortcuts import render
from django.views import View


class CreateAccount(View):
    """
    A class to handle the create user page's GET and POST requests. As well as retrieve
    a user's credentials from the Account database.
    """

    def get(self, request):
        """GET method for create user page."""
        return render(request, "create_account.html")

    def post(self, request):
        """POST method for create user page."""
        return render(request, "create_account.html")
