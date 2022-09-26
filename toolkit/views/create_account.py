from typing import Optional
from django.shortcuts import render
from django.views import View
from django.forms import Form, CharField, EmailField, PasswordInput, TextInput
from django.http.request import HttpRequest
from django.http.response import HttpResponseRedirect

from toolkit.models import Account


class CreateAccount(View):
    """
    A class to handle the create user page's GET and POST requests. As well as retrieve
    a user's credentials from the Account database.
    """

    def get(self, request: HttpRequest):
        """GET method for create user page."""
        context = {}
        context["form"] = CreateAccountForm()
        return render(request, "create_account.html", context)

    def post(self, request: HttpRequest):
        """POST method for create user page."""
        form = CreateAccountForm(request.POST)
        context = {}
        if form.is_valid():
            create_user(
                form.cleaned_data["username"],
                form.cleaned_data["email"],
                form.cleaned_data["password"],
            )
            return HttpResponseRedirect("/")
        else:
            context["form"] = form
            print("Invalid form")

        return render(request, "create_account.html", context)


class CreateAccountForm(Form):
    email = EmailField(
        required=True,
        widget=TextInput(
            attrs={"class": "form-control", "placeholder": "name@example.com"}
        ),
    )
    username = CharField(
        required=True, widget=TextInput(attrs={"class": "form-control"})
    )
    password = CharField(
        required=True, widget=PasswordInput(attrs={"class": "form-control"})
    )


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
    except Account.DoesNotExist:
        pass

    a = Account(Email=email, Username=username, Password=password)
    a.save()
    return a


def validate_username(username: str):
    raise NotImplementedError()
