import inspect
import logging
import traceback
from dataclasses import dataclass, field
from typing import Any, Optional

from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import View

from toolkit.views.loot_generator.cache_loot import (
    cache_loot,
    delete_cached_loot,
    save_cached_loot,
)
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
        loot_type_list = ["Random"]
        loot_type_list.extend(sorted(self.generator.LOOT_TYPE_DICT))
        self.context["loot_type_list"] = loot_type_list
        self.context["cached"] = False

    def get(self, request: HttpRequest):
        """GET method for the character generation."""
        self.context["data"] = GenerateLootInputs()
        return render(request, "loot_generator.html", self.context)

    def post(self, request: HttpRequest):
        """POST method for create user page."""
        form = GenerateLootInputs.from_dict(request.POST)
        self.context["data"] = form
        self.context["error"] = None
        if not form.is_valid():
            self.context["form"] = form
            return render(request, "loot_generator.html", self.context)
        if request.POST.get("generate_button") is not None:
            try:
                generated = self.generator.generate_loot(
                    generator_key=form.generator_type.value,
                    level=1
                    if form.average_player_level.value == ""
                    else int(form.average_player_level.value),
                    approximate_total_value=0
                    if form.total_hoard_value.value == ""
                    else int(form.total_hoard_value.value),
                    input_loot_type=form.loot_type.value,
                )
                loot_object = generated.get("loot_object")
                self.context["total_value"] = int(loot_object.Total_Value)
                self.context["money"] = int(loot_object.Money)
                generated_list = generated.get("armors")
                generated_list.extend(generated.get("weapons"))
                generated_list.extend(generated.get("general"))
                generated_list.extend(generated.get("magic"))
                self.context["generated_list"] = generated_list

                if request.user.is_authenticated:
                    try:
                        cache_loot(
                            user=request.user,
                            loot=loot_object,
                            weapons_output=generated.get("weapons"),
                            armors_output=generated.get("armors"),
                            generic_items_output=generated.get("general"),
                            magic_items_output=generated.get("magic"),
                        )
                        self.context["cached"] = True
                    except TypeError as e:
                        logger.warning(e)
                return render(request, "loot_generator.html", self.context)
            except ValueError as e:
                logger.warning(traceback.format_exc())
                self.context["form"] = form
                self.context["error"] = str(e)
                return render(request, "loot_generator.html", self.context)
        if request.POST.get("save_button") is not None:
            self.context["cached"] = True
            if request.user.is_authenticated:
                save_cached_loot(request.user)
                messages.success(request, "Loot saved successfully!")
            else:
                self.context["form"] = form
            return render(request, "loot_generator.html", self.context)
        if request.POST.get("clear_button") is not None:
            if request.user.is_authenticated:
                delete_cached_loot(request.user)
            self.context["data"] = GenerateLootInputs()
            return render(request, "loot_generator.html", self.context)
        return render(request, "loot_generator.html", self.context)


@dataclass
class GenerateLootInputs:
    """Class which holds all the user intractable for the loot generator page"""

    generator_type: Element = field(default_factory=lambda: Element("Random"))
    loot_type: Element = field(default_factory=lambda: Element("Random"))
    total_hoard_value: Element = field(default_factory=Element)  # Optional
    average_player_level: Element = field(default_factory=Element)  # Optional

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
        if (
            self.generator_type.value
            not in Loot_Generator().get_all_random_generators()
        ):
            return False
        if (
            self.loot_type.value not in Loot_Generator.LOOT_TYPE_DICT
            and self.loot_type.value != "Random"
        ):
            return False
        if self.total_hoard_value.value != "" and int(self.total_hoard_value.value) < 0:
            return False
        if (
            self.average_player_level.value != ""
            and not 0 < int(self.average_player_level.value) <= 21
        ):
            return False
        return True
