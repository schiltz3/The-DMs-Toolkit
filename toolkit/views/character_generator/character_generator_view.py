import logging
import traceback

from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import View

from toolkit.models import Character
from toolkit.views.character_generator.cache_character import (
    cache_character,
    delete_cached_character,
    save_cached_character,
)
from toolkit.views.character_generator.character_elements import (
    Element,
    GenerateCharacterInputs,
    GeneratedCharacterOutputs,
)
from toolkit.views.character_generator.character_generator_backend import (
    Character_Generator,
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
        # TODO: Make sure is correct "group"
        self.context["clazz_list"] = sorted(self.generator.CLASS_OPTIONS)
        self.context["background_list"] = sorted(self.generator.BACKGROUND_DICT)
        self.context["race_list"] = sorted(self.generator.RACE_OPTIONS)
        self.context["alignment_list"] = sorted(self.generator.ALIGNMENT_DICT)

        gen_keys = self.generator.get_all_random_generators()
        gen_keys.append("Standard")
        gen_keys = sorted(gen_keys)
        self.context["generator_type_list"] = gen_keys

        self.context["clazz_choices_list"] = self.generator.get_classes()
        self.context["background_choices_list"] = sorted(
            self.generator.BACKGROUND_DICT.get("All")
        )
        self.context["race_choices_list"] = self.generator.get_races()
        self.context["alignment_choices_list"] = sorted(
            self.generator.ALIGNMENT_DICT.get("All")
        )
        self.context["cached"] = False

    def get(self, request: HttpRequest, **kwargs):
        """GET method for the character generation."""
        pk = kwargs.get("pk")
        if pk and request.user.is_authenticated:
            character = Character.objects.filter(pk=pk, Owner=request.user).first()
            if not character:
                messages.warning(
                    request, "The character you are trying to view can not be found"
                )
            else:
                self.context["data"] = GenerateCharacterInputs(
                    alignment=Element(character.Alignment),
                    background=Element(character.Background),
                    character_name=Element(character.Name),
                    clazz=Element(character.Class),
                    experience_points=Element(character.Experience),
                    player_name=Element(character.Owner),
                    race=Element(character.Race),
                )
                out = GeneratedCharacterOutputs(
                    charisma=character.Charisma,
                    constitution=character.Constitution,
                    dexterity=character.Dexterity,
                    intelligence=character.Intelligence,
                    strength=character.Strength,
                    wisdom=character.Wisdom,
                    calculate=True,
                )
                proficiencies = character.Character_Proficiencies.aggregate()
                if proficiencies:
                    print(proficiencies)
                    out.update_proficiencies_from_dict(request.POST)
                self.context["out"] = out
        else:
            self.context["data"] = GenerateCharacterInputs(
                player_name=Element(request.user.get_username())
            )
            self.context["out"] = GeneratedCharacterOutputs(calculate=False)
        return render(request, "character_generator.html", self.context)

    def post(self, request: HttpRequest, **kwargs):
        """POST method for the character generation."""

        form = GenerateCharacterInputs.from_dict(request.POST)
        self.context["data"] = form
        if not form.is_valid():
            self.context["form"] = form
            self.context["data"] = GenerateCharacterInputs(
                player_name=Element(request.user.get_username())
            )
            self.context["out"] = GeneratedCharacterOutputs(calculate=False)
            return render(request, "character_generator.html", self.context)
        if request.POST.get("generate_button") is not None:
            try:
                generator_key = "Random"

                try:
                    form.race.value = self.generator.generate_race(
                        form.race.value, generator_key
                    )
                except ValueError:
                    form.race.error = "Unable to generate Race"
                try:
                    form.clazz.value = self.generator.generate_class(
                        form.clazz.value, generator_key
                    )
                except (ValueError, RuntimeError):
                    form.clazz.error = "Unable to generate Class"
                alignment = form.alignment.value
                if alignment in self.generator.ALIGNMENT_DICT:
                    try:
                        form.alignment.value = self.generator.generate_alignment(
                            Character_Generator.ALIGNMENT_DICT[alignment],
                            generator_key,
                        )
                    except ValueError:
                        form.alignment.error = "Unable to generate Alignment"
                background = form.background.value
                if background in self.generator.BACKGROUND_DICT:
                    try:
                        form.background.value = self.generator.generate_background(
                            Character_Generator.BACKGROUND_DICT[background],
                            generator_key,
                        )
                    except ValueError:
                        form.background.error = "Unable to generate Background"

                stat_generator_key = form.generator_type.value
                try:
                    if stat_generator_key == "Standard":
                        stats = Character_Generator.arrange_stats(
                            form.clazz.value, Character_Generator.STANDARD_ARRAY
                        )
                    else:
                        stats = self.generator.generate_stat_list(stat_generator_key)
                        stats = self.generator.arrange_stats(form.clazz.value, stats)
                except ValueError:
                    form.generator_type.error = "Unable to use specified generator"

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
                    try:
                        cache_character(
                            request.user,
                            char_input=self.context["data"],
                            char_output=output,
                        )
                        self.context["cached"] = True
                    except TypeError as e:
                        logger.warning(e)
                return render(request, "character_generator.html", self.context)
            except (ValueError, RuntimeError):
                logger.warning(traceback.format_exc())
                self.context["form"] = form
                messages.error(request, "Unable to generate character")
                return render(request, "character_generator.html", self.context)

        if request.POST.get("save_button") is not None:
            character = None
            if request.user.is_authenticated:
                character = save_cached_character(request.user)
                self.context["cached"] = False
            self.context["data"] = GenerateCharacterInputs.from_dict(request.POST)
            if character:
                self.context["out"] = GeneratedCharacterOutputs(
                    calculate=True,
                    strength=character.Strength,
                    dexterity=character.Dexterity,
                    constitution=character.Constitution,
                    intelligence=character.Intelligence,
                    wisdom=character.Wisdom,
                    charisma=character.Charisma,
                ).update_proficiencies_from_dict(request.POST)
                messages.success(request, "Character saved successfully!")
            else:
                self.context["out"] = GeneratedCharacterOutputs(calculate=False)
            return render(request, "character_generator.html", self.context)

        if (
            request.POST.get("clear_button") is not None
            or request.POST.get("close_save_button") is not None
        ):
            if request.user.is_authenticated:
                delete_cached_character(request.user)
                self.context["cached"] = False
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
