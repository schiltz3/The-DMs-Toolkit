import inspect
from dataclasses import dataclass, field
from typing import Any, Optional

from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import View

from toolkit.views.character_generator.character_generation import Character_Generator


@dataclass
class Element:
    """Contains the value and error to display in templates"""

    value: Any = None
    error: Optional[str] = None

    def __repr__(self):
        return f"Data: {self.value} Error: {self.error if self.error else ''}"


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
        print(request.POST.get("character_name"))

        print(request.POST)

        form = GenerateCharacterInputs.from_dict(request.POST)
        print(form)
        self.context["data"] = form
        self.context["error"] = None
        if not form.is_valid():
            self.context["form"] = form
            print("Invalid form")
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
                self.context["out"] = output
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


@dataclass
class GenerateCharacterInputs:
    """Class which holds all the user intractable for the character generator page"""

    character_name: Element = field(default_factory=lambda: Element(""))
    player_name: Element = field(default_factory=Element)  # Optional
    clazz: Element = field(default_factory=lambda: Element("All"))
    background: Element = field(default_factory=lambda: Element("All"))
    race: Element = field(default_factory=lambda: Element("All"))
    alignment: Element = field(default_factory=lambda: Element("All"))
    generator_type: Element = field(default_factory=lambda: Element("3D6"))
    experience_points: Element = field(default_factory=lambda: Element(0))

    # valid_data: dict[str, Any] = field(default_factory=dict)

    @classmethod
    def from_dict(cls, env: dict[str, Any]):
        """Takes a dictionary, and pulls out the correct args for GenerateCharacterInputs
        then returns a new GenerateCharacterInputs with the args filled out
        Args:
            env (dict[str, Any]): Any dictionary

        Returns:
            GeneratedCharacterInputs: new GeneratedCharacterInputs with args from env
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
        self.character_name.value = self.character_name.value.strip()
        return True


@dataclass
class Stat:
    value: int = 0
    repr: str = ""
    proficiency: int = 0

    def sk_to_str(self):
        val = self.value + self.proficiency
        pos = "+" if self.value + val >= 0 else "-"
        self.repr = f"{pos} {abs(val)}"
        return self


class GeneratedCharacterOutputs:
    """Contain all the non-user intractable elements of the page"""

    def __init__(
        self,
        calculate=True,
        strength=0,
        dexterity=0,
        constitution=0,
        intelligence=0,
        wisdom=0,
        charisma=0,
        proficiency=0,
    ):
        self.strength = strength
        self.dexterity = dexterity
        self.constitution = constitution
        self.intelligence = intelligence
        self.wisdom = wisdom
        self.charisma = charisma

        self.proficiency: Stat = Stat(value=proficiency)
        self.stat_speed: int = 0
        self.stat_hit_points: int = 0
        self.stat_hit_dice: int = 0

        self.stats = {
            "stat_initiative": Stat(),
            "mod_strength": Stat(),
            "mod_dexterity": Stat(),
            "mod_constitution": Stat(),
            "mod_intelligence": Stat(),
            "mod_wisdom": Stat(),
            "mod_charisma": Stat(),
            "st_strength": Stat(),
            "st_dexterity": Stat(),
            "st_constitution": Stat(),
            "st_intelligence": Stat(),
            "st_wisdom": Stat(),
            "st_charisma": Stat(),
            "sk_acrobatics": Stat(),
            "sk_animal_handling": Stat(),
            "sk_arcana": Stat(),
            "sk_athletics": Stat(),
            "sk_deception": Stat(),
            "sk_history": Stat(),
            "sk_insight": Stat(),
            "sk_intimidation": Stat(),
            "sk_investigation": Stat(),
            "sk_medicine": Stat(),
            "sk_nature": Stat(),
            "sk_perception": Stat(),
            "sk_performance": Stat(),
            "sk_persuasion": Stat(),
            "sk_religion": Stat(),
            "sk_sleight_of_hand": Stat(),
            "sk_stealth": Stat(),
            "sk_survival": Stat(),
        }
        if calculate is True:
            self.calculate()

    def calculate(self):
        self.stats["mod_strength"] = Character_Generator.calculate_ability_modifier(
            self.strength
        )
        self.stats["mod_dexterity"] = Character_Generator.calculate_ability_modifier(
            self.dexterity
        )
        self.stats["mod_constitution"] = Character_Generator.calculate_ability_modifier(
            self.constitution
        )
        self.stats["mod_intelligence"] = Character_Generator.calculate_ability_modifier(
            self.intelligence
        )
        self.stats["mod_wisdom"] = Character_Generator.calculate_ability_modifier(
            self.wisdom
        )
        self.stats["mod_charisma"] = Character_Generator.calculate_ability_modifier(
            self.charisma
        )

        self.stats["st_strength"] = self.mod_strength
        self.stats["st_dexterity"] = self.mod_dexterity
        self.stats["st_constitution"] = self.mod_constitution
        self.stats["st_intelligence"] = self.mod_intelligence
        self.stats["st_charisma"] = self.mod_charisma
        self.stats["st_wisdom"] = self.mod_wisdom

        # TODO: Add proficiency bonus to initiative
        self.stats["stat_initiative"] = self.mod_dexterity

        self.stats["sk_athletics"] = self.mod_strength

        self.stats["sk_acrobatics"] = self.mod_dexterity
        self.stats["sk_sleight_of_hand"] = self.mod_dexterity
        self.stats["sk_stealth"] = self.mod_dexterity

        self.stats["sk_animal_handling"] = self.mod_wisdom
        self.stats["sk_insight"] = self.mod_wisdom
        self.stats["sk_medicine"] = self.mod_wisdom
        self.stats["sk_perception"] = self.mod_wisdom
        self.stats["sk_survival"] = self.mod_wisdom

        self.stats["sk_deception"] = self.mod_charisma
        self.stats["sk_intimidation"] = self.mod_charisma
        self.stats["sk_performance"] = self.mod_charisma
        self.stats["sk_persuasion"] = self.mod_charisma
        self.stats["sk_religion"] = self.mod_intelligence

        for v in self.stats.values():
            v.sk_to_str()

        return self
