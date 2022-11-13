import logging
from django.contrib.auth.models import User

from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import View

from toolkit.views.character_generator.character_generation import Character_Generator
from toolkit.views.character_generator.cache_character import (
    cache_character,
    retrieve_cached_character,
)
from toolkit.views.character_generator.character_elements import (
    Element,
    GenerateCharacterInputs,
    GeneratedCharacterOutputs,
)

logger = logging.getLogger(__name__)


class CharacterGenerator(View):
    """
    A class to provide a  page for users visiting the site to
    generate characters.
    """

    def __init__(self, **kwargs):
        super(CharacterGenerator, self).__init__(**kwargs)

        self.context: dict[str, any] = {}
        self.generator = Character_Generator()
        self.context["out"] = GeneratedCharacterOutputs(calculate=True)
        self.context["clazz_list"] = sorted(self.generator.CLASS_DICT)
        self.context["background_list"] = sorted(self.generator.BACKGROUND_DICT)
        self.context["race_list"] = sorted(self.generator.RACE_DICT)
        self.context["alignment_list"] = sorted(self.generator.ALIGNMENT_DICT)

        gen_keys = self.generator.get_all_random_generators()
        gen_keys.append("Standard")
        gen_keys = sorted(gen_keys)
        self.context["generator_type_list"] = gen_keys

        self.context["clazz_choices_list"] = sorted(
            self.generator.CLASS_DICT.get("All")
        )
        self.context["background_choices_list"] = sorted(
            self.generator.BACKGROUND_DICT.get("All")
        )
        self.context["race_choices_list"] = sorted(self.generator.RACE_DICT.get("All"))
        self.context["alignment_choices_list"] = sorted(
            self.generator.ALIGNMENT_DICT.get("All")
        )

    def get(self, request: HttpRequest):
        """GET method for the character generation."""
        self.context["data"] = GenerateCharacterInputs(
            player_name=Element(request.user.get_username())
        )
        self.context["out"] = GeneratedCharacterOutputs(calculate=False)
        return render(request, "character_generator.html", self.context)

    def post(self, request: HttpRequest):
        """POST method for create user page."""

        logger.info(request.POST)

        form = GenerateCharacterInputs.from_dict(request.POST)
        self.context["data"] = form
        self.context["error"] = None
        if not form.is_valid():
            self.context["form"] = form
            logger.info("Invalid form")
            self.context["data"] = GenerateCharacterInputs(
                player_name=Element(request.user.get_username())
            )
            self.context["out"] = GeneratedCharacterOutputs(calculate=False)
            return render(request, "character_generator.html", self.context)
        if request.POST.get("generate_button") is not None:
            try:
                generator_key = "Random"
                stat_generator_key = form.generator_type.value

                race = form.race.value
                if race in self.generator.RACE_DICT:
                    form.race.value = self.generator.generate_race(
                        Character_Generator.RACE_DICT[race], generator_key
                    )
                clazz = form.clazz.value
                if clazz in self.generator.CLASS_DICT:
                    form.clazz.value = self.generator.generate_class(
                        Character_Generator.CLASS_DICT[clazz], generator_key
                    )
                alignment = form.alignment.value
                if alignment in self.generator.ALIGNMENT_DICT:
                    form.alignment.value = self.generator.generate_alignment(
                        Character_Generator.ALIGNMENT_DICT[alignment],
                        generator_key,
                    )
                background = form.background.value
                if background in self.generator.BACKGROUND_DICT:
                    form.background.value = self.generator.generate_background(
                        Character_Generator.BACKGROUND_DICT[background],
                        generator_key,
                    )

                if stat_generator_key == "Standard":
                    stats = Character_Generator.Arrange(
                        form.clazz.value, Character_Generator.STANDARD_ARRAY
                    )
                else:
                    stats = self.generator.generate_stat_list(stat_generator_key)

                output = GeneratedCharacterOutputs(
                    calculate=True,
                    strength=stats[0],
                    dexterity=stats[1],
                    constitution=stats[2],
                    intelligence=stats[3],
                    wisdom=stats[4],
                    charisma=stats[5],
                )
                output.update_proficiencies_from_dict(request.POST)
                self.context["out"] = output

                if request.user.is_authenticated:
                    if type(request.user) is not User:
                        raise TypeError(
                            f"User is of class {type(request.user)} when it should be User. Is user not logged in?"
                        )
                    try:
                        cache_character(
                            request.user, input=self.context["data"], output=output
                        )
                    except TypeError as e:
                        logger.warning(e)
                return render(request, "character_generator.html", self.context)
            except ValueError as e:
                self.context["form"] = form
                self.context["error"] = str(e)
                return render(request, "character_generator.html", self.context)

        if request.POST.get("save_button") is not None:
            return render(request, "character_generator.html", self.context)
        if request.POST.get("clear_button") is not None:
            self.context["data"] = GenerateCharacterInputs(
                player_name=Element(request.user.get_username())
            )
            self.context["out"] = GeneratedCharacterOutputs(calculate=False)
            return render(request, "character_generator.html", self.context)

        self.context["form"] = form
        self.context["data"] = GenerateCharacterInputs(
            player_name=Element(request.user.get_username())
        )
        self.context["out"] = GeneratedCharacterOutputs(calculate=False)
        return render(request, "character_generator.html", self.context)
