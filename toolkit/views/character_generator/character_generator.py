from dataclasses import InitVar, dataclass, field
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
        self.context["out"] = GeneratedCharacterOutputs(calculate=True)
        self.context["clazz_list"] = sorted(self.generator.CLASS_DICT)
        self.context["background_list"] = sorted(self.generator.BACKGROUND_LIST)
        self.context["race_list"] = sorted(self.generator.RACE_DICT)
        self.context["alignment_list"] = sorted(self.generator.ALIGNMENT_DICT)

    def get(self, request: HttpRequest):
        """GET method for the character generation."""
        self.context["data"] = GenerateCharacterInputs()
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
        if form.is_valid():
            try:
                if request.POST.get("generate_button") is not None:
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

                elif request.POST.get("save_button") is not None:
                    return render(request, "character_generator.html", self.context)
                elif request.POST.get("export_button") is not None:
                    return render(request, "character_generator.html", self.context)
            except ValueError as e:
                self.context["form"] = form
                self.context["error"] = str(e)
                return render(request, "character_generator.html", self.context)

        self.context["form"] = form
        print("Invalid form")
        return render(request, "character_generator.html", self.context)


@dataclass
class GenerateCharacterInputs:
    character_name: Element = field(default_factory=Element)
    player_name: Element = field(default_factory=Element)  # Optional
    clazz: Element = field(default_factory=lambda: Element("All"))
    background: Element = field(default_factory=lambda: Element("Acolyte"))
    race: Element = field(default_factory=lambda: Element("All"))
    alignment: Element = field(default_factory=lambda: Element("All"))
    experience_points: Element = field(default_factory=lambda: Element(0))

    @classmethod
    def from_dict(cls, env: dict[str, Any]):
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
    calculate: InitVar[bool] = True
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
    mod_charisma: str = "+0"

    proficency: str = "+0"

    st_strength: str = "+0"
    st_dexterity: str = "+0"
    st_constitution: str = "+0"
    st_intelligence: str = "+0"
    st_wisdom: str = "+0"
    st_charisma: str = "+0"

    stat_speed: int = 0
    stat_initiative: str = "0"
    stat_hit_points: int = 0
    stat_hit_dice: int = 0

    sk_acrobatics: str = "+0"
    sk_animal_handling: str = "+0"
    sk_arcana: str = "+0"
    sk_athletics: str = "+0"
    sk_deception: str = "+0"
    sk_history: str = "+0"
    sk_insight: str = "+0"
    sk_intimidation: str = "+0"
    sk_investigation: str = "+0"
    sk_medicine: str = "+0"
    sk_nature: str = "+0"
    sk_perception: str = "+0"
    sk_performance: str = "+0"
    sk_persuasion: str = "+0"
    sk_religion: str = "+0"
    sk_sleight_of_hand: str = "+0"
    sk_stealth: str = "+0"
    sk_survival: str = "+0"

    def __post_init__(self, calculate: bool):
        if calculate is False:
            return
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
        self.st_strength = self.mod_strength

        self.st_dexterity = self.mod_strength
        self.st_constitution = self.mod_constitution
        self.st_intelligence = self.mod_intelligence
        self.st_charisma = self.mod_charisma

        # TODO: Add proficiency bonus to initiative
        self.stat_initiative = self.mod_dexterity

        # TODO: Add proficiency bonuses to these if proficient

        self.sk_athletics = self.mod_strength

        self.sk_acrobatics = self.mod_dexterity
        self.sk_sleight_of_hand = self.mod_dexterity
        self.sk_stealth = self.mod_dexterity

        self.sk_arcana = self.mod_intelligence
        self.sk_history = self.mod_intelligence
        self.sk_investigation = self.mod_intelligence
        self.sk_nature = self.mod_intelligence
        self.sk_religion = self.mod_intelligence

        self.sk_animal_handling = self.mod_wisdom
        self.sk_insight = self.mod_wisdom
        self.sk_medicine = self.mod_wisdom
        self.sk_perception = self.mod_wisdom
        self.sk_survival = self.mod_wisdom

        self.sk_deception = self.mod_charisma
        self.sk_intimidation = self.mod_charisma
        self.sk_performance = self.mod_charisma
        self.sk_persuasion = self.mod_charisma
