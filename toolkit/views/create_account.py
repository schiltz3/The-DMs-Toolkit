from typing import Optional
from django.shortcuts import render
from django.views import View
from django.forms import Form, CharField, EmailField, PasswordInput, TextInput

from toolkit.models import Account
from django.db.models import Model
from toolkit.views.custom_text_input import CustomTextInput


class CreateAccount(View):
    """
    A class to handle the create user page's GET and POST requests. As well as retrieve
    a user's credentials from the Account database.
    """

    def get(self, request):
        """GET method for create user page."""
        context = {}
        context["form"] = CreateAccountForm()
        return render(request, "create_account.html", context)

    def post(self, request):
        """POST method for create user page."""

        return render(request, "create_account.html")


class CreateAccountForm(Form):
    email = EmailField(
        required=True, widget=CustomTextInput(attrs={"placeholder": "name@example.com"})
    )
    username = CharField(required=True, widget=CustomTextInput())
    password = CharField(required=True, widget=CustomTextInput())


def create_user(username: str, email: str, password: str) -> Optional[Account]:
    """Create a new user object and save in database if one does not already exist for that email

    Args:
        username (str): A valid username containing only alpha-numeric characters
        email (str): A valid email
        password (str): A valid password

    Returns:
        Optional[Account]: Returns None if account already exists, otherwise returns the new account
    """
    try:
        Account.objects.get(Email=email)
        return None
    except Model.DoesNotExist:
        pass

    a = Account(Email=email, Username=username, Password=password)
    a.save()
    return a


def validate_username(username: str):
    raise NotImplementedError()
