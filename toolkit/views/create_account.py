from typing import Any, Optional

from django.forms import CharField, EmailField, Form, PasswordInput, TextInput
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

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
                email=form.cleaned_data["email"],
                permanent=True,
            )
        else:
            context["form"] = form
            print("Invalid form")

        return render(request, "create_account.html", context)


class CreateAccountForm(Form):
    username = CharField(
        required=True, widget=TextInput(attrs={"class": "form-control"})
    )
    email = EmailField(
        required=True,
        widget=TextInput(
            attrs={"class": "form-control", "placeholder": "name@example.com"}
        ),
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
        raise ValueError(f"Account {email} already exists")
    except Account.DoesNotExist:
        pass

    a = Account(Email=email, Username=username, Password=password)
    print(a)
    a.save()
    return a
