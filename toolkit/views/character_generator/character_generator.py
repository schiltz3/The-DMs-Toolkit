from dataclasses import dataclass
from turtle import back
from django.shortcuts import render
from django.views import View
import inspect

from django.forms import (
    CharField,
    Form,
    TextInput,
    Select,
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

        self.context: dict[str, any] = {}
        self.generator = Character_Generator()
        self.context["clazz_list"] = sorted(self.generator.CLASS_DICT)
        self.context["background_list"] = sorted(self.generator.BACKGROUND_LIST)
        self.context["race_list"] = sorted(self.generator.RACE_DICT)
        self.context["alignment_list"] = sorted(self.generator.ALIGNMENT_DICT)

    def get(self, request: HttpRequest):
        """GET method for the character generation."""
        """GET method for create user page."""
        class_keys = self.generator.CLASS_DICT.keys()
        class_keys_type = type(self.generator.CLASS_DICT.keys())
        print(class_keys_type)
        print(class_keys)
        self.context["data"] = GenerateCharacterData(
            clazz="All", background="All", race="All", alignment="All"
        )
        # self.context["form"] = GenerateCharacterForm({"clazz": "All"})

        return render(request, "character_generator.html", self.context)

    def post(self, request: HttpRequest):
        """POST method for create user page."""

        form = GenerateCharacterData.from_form(request.POST)
        self.context["data"] = form
        self.context["error"] = None
        if form.is_valid():
            try:
                ...
            except ValueError as e:
                self.context["form"] = form
                self.context["error"] = str(e)
                return render(request, "create_account.html", self.context)

        self.context["form"] = form
        print("Invalid form")
        return render(request, "character_generator.html", self.context)


@dataclass
class GenerateCharacterData:
    name: str = ""
    clazz: str = ""
    background: str = ""
    player_name: str = ""
    race: str = ""
    alignment: str = ""
    experience_points: int = 0

    strength: int = 0
    dexterity: int = 0
    constitution: int = 0
    intelligence: int = 0
    wisdom: int = 0
    charisma: int = 0

    @classmethod
    def from_form(cls, env):
        return cls(
            **{k: v for k, v in env.items() if k in inspect.signature(cls).parameters}
        )

    def is_valid(self):
        return True


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
