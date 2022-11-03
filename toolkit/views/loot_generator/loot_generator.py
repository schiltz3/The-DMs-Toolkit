import inspect
import logging
import traceback
from dataclasses import dataclass, field
from typing import Any, Optional

from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import View

from toolkit.views.loot_generator.loot_generation import Loot_Generator

logger = logging.getLogger(__name__)


class Element:
    """Contains the value and error to display in templates"""

    def __init__(self, data: Any = "", error: Optional[str] = None):
        self.value = data
        self.error = error

    def __repr__(self):
        return f"Data: {self.value} Error: {self.error if self.error else ''}"


class LootGenerator(View):
    """
    A class to provide a page for users visiting the site to
    generate loot.
    """

    def __init__(self, **kwargs):
        super(LootGenerator, self).__init__(**kwargs)

        self.context: dict[str, any] = {}
        self.generator = Loot_Generator()
        gen_keys = self.generator.get_all_random_generators()
        gen_keys = sorted(gen_keys)
        self.context["loot_generator_list"] = gen_keys
        self.context["loot_type_list"] = sorted(self.generator.LOOT_TYPE_DICT)

    def get(self, request: HttpRequest):
        """GET method for the character generation."""
        self.context["data"] = GenerateLootInputs()
        return render(request, "loot_generator.html", self.context)

    def post(self, request: HttpRequest):
        """POST method for create user page."""
        form = GenerateLootInputs.from_dict(request.POST)
        self.context["data"] = form
        self.context["error"] = None
        if form.is_valid():
            try:
                if request.POST.get("generate_button") is not None:
                    if request.user.is_authenticated:
                        current_user = request.user
                    else:
                        current_user = None
                    generated = self.generator.generate_loot(
                        current_user=current_user,
                        generator_key=form.generator_type.value,
                        level=int(form.average_player_level.value),
                        approximate_total_value=int(form.total_hoard_value.value),
                        input_loot_type=form.loot_type.value,
                    )
                    loot_object = generated.get("loot_object")
                    self.context["total_value"] = int(loot_object.Total_Value)
                    self.context["money"] = int(loot_object.Money)
                    generated_list = generated.get("armor")
                    generated_list.extend(generated.get("weapons"))
                    generated_list.extend(generated.get("general0"))
                    generated_list.extend(generated.get("magic"))
                    self.context["generated_list"] = generated_list
                    return render(request, "loot_generator.html", self.context)
                if request.POST.get("save_button") is not None:
                    return render(request, "loot_generator.html", self.context)
                if request.POST.get("clear_button") is not None:
                    self.context["data"] = GenerateLootInputs()
                    return render(request, "loot_generator.html", self.context)
            except ValueError as e:
                logger.warning(traceback.format_exc())
                self.context["form"] = form
                self.context["error"] = str(e)
                return render(request, "loot_generator.html", self.context)

        self.context["form"] = form
        print("Invalid form")
        return render(request, "loot_generator.html", self.context)


@dataclass
class GenerateLootInputs:
    """Class which holds all the user intractable for the loot generator page"""

    generator_type: Element = field(default_factory=lambda: Element("Random"))
    loot_type: Element = field(default_factory=lambda: Element("Random"))
    total_hoard_value: Element = field(default_factory=lambda: Element(0))
    average_player_level: Element = field(default_factory=lambda: Element(0))

    @classmethod
    def from_dict(cls, env: dict[str, Any]):
        """Takes a dictionary, and pulls out the correct args for GenerateLootInputs
        then returns a new GenerateLootInputs with the args filled out
        Args:
            env (dict[str, Any]): Any dictionary

        Returns:
            GeneratedLootInputs: new GeneratedCharacterInputs with args from env
        """
        return cls(
            **{
                k: Element(v)
                for k, v in env.items()
                if k in inspect.signature(cls).parameters
            }
        )

    def is_valid(self) -> bool:
        """Determine if Dataclass holds all valid data

        Returns:
            bool: Tru if dataclass holds valid data
        """
        return True
