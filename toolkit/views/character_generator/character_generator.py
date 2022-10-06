from django.shortcuts import render
from django.views import View
from typing import Any, Optional

from django.contrib.auth.models import User
from django.forms import (
    CharField,
    Form,
    TextInput,
    Select,
    TypedChoiceField,
    ChoiceField,
)
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from toolkit.views.character_generator.character_generation import Character_Generator


class CharacterGenerator(View):
    """
    A class to provide a  page for users visiting the site to
    generate characters.
    """

    def __init__(self, **kwargs):
        super(CharacterGenerator, self).__init__(**kwargs)

        self.context: dict[str, any] = {
            "strength": 0,
            "dexterity": 0,
            "constitution": 0,
            "intelligence": 0,
            "wisdom": 0,
            "charisma": 0,
        }
        self.generator = Character_Generator()

    def get(self, request: HttpRequest):
        """GET method for the character generation."""
        """GET method for create user page."""
        class_keys = self.generator.CLASS_DICT.keys()
        class_keys_type = type(self.generator.CLASS_DICT.keys())
        print(class_keys_type)
        print(class_keys)
        self.context["form"] = GenerateCharacterForm({"clazz": "All"})

        return render(request, "character_generator.html", self.context)

    def post(self, request: HttpRequest):
        """POST method for create user page."""
        form = GenerateCharacterForm(request.POST)
        self.context["error"] = None
        if form.is_valid():
            try:
                ...
            except ValueError as e:
                self.context["form"] = form
                self.context["error"] = str(e)
                return render(request, "create_account.html", self.context)

            return redirect(
                "confirm_account_creation",
                email=form.cleaned_data["username"],
                permanent=True,
            )
        self.context["form"] = form
        print("Invalid form")
        return render(request, "character_generator.html", self.context)


class GenerateCharacterForm(Form):
    """Creates a new form for the Generate Character  template.
    Takes the POST request returned as an argument to create a new filled out form

    Args:
        username (str):
        email (str):
        password (str):
    """

    name = CharField(
        required=False,
        widget=TextInput(
            attrs={
                "class": "big form-control",
            }
        ),
    )
    clazz = ChoiceField(
        required=False,
        # widget=Select(
        #     attrs={"class": "dropdown btn dropdown-toggle", "maxlength": 50},
        # ),
        choices=[(key, key) for key in Character_Generator.CLASS_DICT.keys()],
    )
    background = CharField(
        required=False,
        widget=Select(attrs={"class": " form-control", "maxlength": 50}),
    )
    player_name = CharField(
        required=False,
        widget=Select(attrs={"class": " form-control", "maxlength": 50}),
    )
    race = CharField(
        required=False,
        widget=Select(attrs={"class": " form-control", "maxlength": 50}),
    )
    alignment = CharField(
        required=False,
        widget=Select(attrs={"class": " form-control", "maxlength": 50}),
    )
    experience_points = CharField(
        required=False,
        widget=Select(attrs={"class": " form-control", "maxlength": 50}),
    )
