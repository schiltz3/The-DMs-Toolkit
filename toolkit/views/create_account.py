from typing import Any, Optional

from django.contrib.auth.models import User
from django.forms import CharField, EmailField, Form, PasswordInput, TextInput
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views import View


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
        context: dict[str, Any] = {"error": None}
        if form.is_valid():
            try:
                create_user(
                    form.cleaned_data["username"],
                    form.cleaned_data["email"],
                    form.cleaned_data["password"],
                )
            except ValueError as e:
                context["form"] = form
                context["error"] = str(e)
                return render(request, "create_account.html", context)

            return redirect(
                "confirm_account_creation",
                email=form.cleaned_data["username"],
                permanent=True,
            )
        context["form"] = form
        print("Invalid form")

        return render(request, "create_account.html", context)


class CreateAccountForm(Form):
    """Creates a new form for the Create Account template.
    Takes the POST request returned as an argument to create a new filled out form

    Args:
        username (str):
        email (str):
        password (str):
    """

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


def create_user(username: str, email: str, password: str) -> Optional[User]:
    """Create a new user object and save in database
    if one does not already exist for that email

    Args:
        username (str): A valid username containing only alpha-numeric characters
        email (str): A valid email
        password (str): A valid password


    Raises:
        ValueError: Raises an error if no user is found

    Returns:
        Optional[Account]: Returns None if account already exists,
        otherwise returns the new account
    """
    try:
        User.objects.get(username=username)
        raise ValueError(
            f"User {username} already exists please pick a different username"
        )
    except User.DoesNotExist:
        pass

    a = User(email=email, username=username, password=password)
    a.save()
    return a
