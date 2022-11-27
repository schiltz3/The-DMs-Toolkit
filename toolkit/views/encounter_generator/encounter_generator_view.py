import inspect
import logging
import traceback
from dataclasses import dataclass, field
from typing import Any, Optional

from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import View

from toolkit.models import GeneratedEncounter, Monster, Tag
from toolkit.views.encounter_generator.cache_encounter import (
    cache_encounter,
    delete_cached_encounter,
    save_cached_encounter,
)
from toolkit.views.encounter_generator.encounter_generator_backend import (
    Encounter_Generator,
)

logger = logging.getLogger(__name__)


class Element:
    """Contains the value and error to display in templates"""

    def __init__(self, data: Any = "", error: Optional[str] = None):
        self.value = data
        self.error = error

    def __repr__(self):
        return f"Data: {self.value} Error: {self.error if self.error else ''}"


class EncounterGenerator(View):
    """
    A class to provide a page for users visiting the site to
    generate encounters.
    """

    def __init__(self, **kwargs):
        super(EncounterGenerator, self).__init__(**kwargs)

        self.context: dict[str, any] = {}
        self.generator = Encounter_Generator()
        gen_keys = self.generator.get_all_random_generators()
        gen_keys = sorted(gen_keys)
        self.context["encounter_generator_list"] = gen_keys
        encounter_type_list = ["Random"]
        encounter_type_list.extend(sorted(self.generator.ENCOUNTER_TYPE_LIST))
        self.context["encounter_type_list"] = encounter_type_list
        encounter_tags_list = ["All"]
        encounter_tags_list.extend(Tag.objects.all())
        self.context["encounter_tags_list"] = encounter_tags_list
        self.context["cached"] = False

    def get(self, request: HttpRequest):
        """GET method for the encounter generation."""
        self.context["data"] = GenerateEncounterInputs()
        return render(request, "encounter_generator.html", self.context)

    def post(self, request: HttpRequest):
        """POST method for the encounter generation."""
        form = GenerateEncounterInputs.from_dict(request.POST)
        self.context["data"] = form
        self.context["error"] = None
        if not form.is_valid():
            self.context["form"] = form
            return render(request, "encounter_generator.html", self.context)
        if request.POST.get("generate_button") is not None:
            try:
                generated = self.generator.generate_encounter(
                    average_level=1
                    if form.average_player_level.value == ""
                    else int(form.average_player_level.value),
                    encounter_type=form.encounter_type.value,
                    tags=None
                    if form.encounter_tags.value == "All"
                    else request.POST.getlist("encounter_tags"),
                    generator_key=form.generator_type.value,
                    loot_generate=False,
                )
                encounter_object: GeneratedEncounter = generated.get("encounter_object")
                self.context["total_monsters"] = int(generated.get("monster_count"))
                generated_list: list[Monster] = generated.get("monsters")
                generated_list.sort(key=lambda x: x.Name)
                generated_dict: dict[Monster, int] = dict()
                for i in generated_list:
                    generated_dict[i] = generated_dict.get(i, 0) + 1
                self.context["generated_dict"] = generated_dict
                if request.user.is_authenticated:
                    try:
                        cache_encounter(
                            user=request.user,
                            encounter=encounter_object,
                            monster_output=generated.get("monsters"),
                        )
                        self.context["cached"] = True
                    except TypeError as e:
                        logger.warning(e)
                return render(request, "encounter_generator.html", self.context)
            except ValueError as e:
                logger.warning(traceback.format_exc())
                self.context["form"] = form
                self.context["error"] = str(e)
                return render(request, "encounter_generator.html", self.context)
            except RuntimeError as e:
                messages.success(request, "No monsters with those tags at your levels.")
                logger.warning(traceback.format_exc())
                self.context["form"] = form
                self.context["error"] = str(e)
                return render(request, "encounter_generator.html", self.context)
        if request.POST.get("save_button") is not None:
            if request.user.is_authenticated:
                save_cached_encounter(request.user)
                messages.success(request, "Encounter saved successfully!")
                self.context["cached"] = False
            else:
                self.context["form"] = form
            return render(request, "encounter_generator.html", self.context)
        if request.POST.get("clear_button") is not None:
            if request.user.is_authenticated:
                delete_cached_encounter(request.user)
                self.context["cached"] = False
            self.context["data"] = GenerateEncounterInputs()
            return render(request, "encounter_generator.html", self.context)
        return render(request, "encounter_generator.html", self.context)


@dataclass
class GenerateEncounterInputs:
    """Class which holds all the user intractable for the encounter generator page"""

    generator_type: Element = field(default_factory=lambda: Element("Random"))
    encounter_type: Element = field(default_factory=lambda: Element("Random"))
    encounter_tags: Element = field(default_factory=lambda: Element("All"))
    average_player_level: Element = field(default_factory=Element)  # Optional

    @classmethod
    def from_dict(cls, env: dict[str, Any]):
        """Takes a dictionary, and pulls out the correct args for GenerateEncounterInputs
        then returns a new GenerateEncounterInputs with the args filled out
        Args:
            env (dict[str, Any]): Any dictionary

        Returns:
            GeneratedEncounterInputs: new GeneratedEncounterInputs with args from env
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
            not in Encounter_Generator().get_all_random_generators()
        ):
            return False
        if (
            self.encounter_type.value not in Encounter_Generator.ENCOUNTER_TYPE_LIST
            and self.encounter_type.value != "Random"
        ):
            return False
        if (
            self.average_player_level.value != ""
            and not 0 < int(self.average_player_level.value) <= 21
        ):
            return False
        return True
