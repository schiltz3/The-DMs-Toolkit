from dataclasses import dataclass, field
from typing import Any, Optional
from django.shortcuts import render
from django.views import View
import inspect

from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import View

from toolkit.views.character_generator.character_generation import Character_Generator


class Element:
    def __init__(self, data: Any = "", error: Optional[str] = None):
        self.value = data
        self.error = error

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
        self.context["out"] = GeneratedCharacterOutputs()
        self.context["clazz_list"] = sorted(self.generator.CLASS_DICT)
        self.context["background_list"] = sorted(self.generator.BACKGROUND_LIST)
        self.context["race_list"] = sorted(self.generator.RACE_DICT)
        self.context["alignment_list"] = sorted(self.generator.ALIGNMENT_DICT)

    def get(self, request: HttpRequest):
        """GET method for the character generation."""
        self.context["data"] = GenerateCharacterInputs()
        return render(request, "character_generator.html", self.context)

    def post(self, request: HttpRequest):
        """POST method for create user page."""
        print(request.POST.get("character_name"))

        print(request.POST)

        form = GenerateCharacterInputs.from_dict(request.POST)
        self.context["data"] = form
        self.context["error"] = None
        if form.is_valid():
            try:
                if request.POST.get("generate_button") is not None:
                    pass
                    generated = Character_Generator.generate(
                        generations_list=[
                            "Stats",
                            "Alignment",
                            "Background",
                            "Race",
                            "Class",
                        ],
                        race_key=form.race.value,
                        class_key=form.clazz.value,
                        alignment_key=form.alignment.value,
                    )
                    stats = generated.get("Stats")
                    if type(stats) is not list:
                        raise ValueError("stats not be list")

                    output = GeneratedCharacterOutputs(
                        strength=stats[0],
                        dexterity=stats[1],
                        constitution=stats[2],
                        intelligence=stats[3],
                        wisdom=stats[4],
                        charisma=stats[5],
                    )
                    self.context["out"] = output
                    return render(request, "character_generator.html", self.context)

                elif request.POST.get("save_button") is not None:
                    pass
                elif request.POST.get("export_button") is not None:
                    pass
                ...
            except ValueError as e:
                self.context["form"] = form
                self.context["error"] = str(e)
                return render(request, "character_generator.html", self.context)

        self.context["form"] = form
        print("Invalid form")
        return render(request, "character_generator.html", self.context)


@dataclass
class GenerateCharacterInputs:
    name: Element = field(default_factory=Element)
    player_name: Element = field(default_factory=Element)  # Optional
    clazz: Element = field(default_factory=lambda: Element("All"))
    background: Element = field(default_factory=lambda: Element("Acolyte"))
    race: Element = field(default_factory=lambda: Element("All"))
    alignment: Element = field(default_factory=lambda: Element("All"))
    experience_points: Element = field(default_factory=lambda: Element(0))

    @classmethod
    def from_dict(cls, env: dict[str, Any]):
        print(env)
        return cls(
            **{
                k: Element(v)
                for k, v in env.items()
                if k in inspect.signature(cls).parameters
            }
        )

    def clean(self):
        if self.clazz.value == "":
            self.clazz.value = "All"
        if self.background.value == "":
            self.background.value = "Acolyte"
        if self.race.value == "":
            self.race.value = "All"
        if self.alignment.value == "":
            self.alignment.value = "All"

    def is_valid(self):
        return True


@dataclass
class GeneratedCharacterOutputs:
    strength: int = 0
    dexterity: int = 0
    constitution: int = 0
    intelligence: int = 0
    wisdom: int = 0
    charisma: int = 0

    mod_strength: str = "+0"
    mod_dexterity: str = "+0"
    mod_constitution: str = "+0"
    mod_intelligence: str = "+0"
    mod_wisdom: str = "+0"
    mod_charisma: str = "+ 0"

    proficency: int = 0

    st_strength: int = 0
    st_dexterity: int = 0
    st_constitution: int = 0
    st_intelligence: int = 0
    st_wisdom: int = 0
    st_charisma: int = 0

    stat_speed: int = 0
    stat_initiative: int = 0
    stat_hit_points: int = 0
    stat_hit_dice: int = 0

    sk_acrobatics: int = 0
    sk_animal_handling: int = 0
    sk_arcana: int = 0
    sk_athletics: int = 0
    sk_deception: int = 0
    sk_history: int = 0
    sk_insight: int = 0
    sk_intimidation: int = 0
    sk_investigation: int = 0
    sk_medicine: int = 0
    sk_nature: int = 0
    sk_perception: int = 0
    sk_performance: int = 0
    sk_persuation: int = 0
    sk_religion: int = 0
    sk_sleight_of_hand: int = 0
    sk_stealth: int = 0
    sk_survival: int = 0

    def __post_init__(self):
        self.mod_strength = Character_Generator.calculate_ability_modifier(
            self.strength
        )
        self.mod_dexterity = Character_Generator.calculate_ability_modifier(
            self.dexterity
        )
        self.mod_constitution = Character_Generator.calculate_ability_modifier(
            self.constitution
        )
        self.mod_intelligence = Character_Generator.calculate_ability_modifier(
            self.intelligence
        )
        self.mod_wisdom = Character_Generator.calculate_ability_modifier(self.wisdom)
        self.mod_charisma = Character_Generator.calculate_ability_modifier(
            self.charisma
        )
