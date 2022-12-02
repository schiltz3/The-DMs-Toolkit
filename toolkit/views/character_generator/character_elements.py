import inspect
from dataclasses import dataclass, field
from typing import Any, Optional

from toolkit.models import Clazz, Race
from toolkit.views.character_generator.character_generator_backend import (
    Character_Generator,
)


@dataclass
class Element:
    """Contains the value and error to display in templates"""

    value: Any = None
    error: Optional[str] = None

    def __repr__(self):
        return f"Data: {self.value} Error: {self.error if self.error else ''}"


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
        if (
            self.generator_type.value != "Standard"
            and self.generator_type.value
            not in Character_Generator().get_all_random_generators()
        ):
            return False
        if (
            self.clazz.value not in Character_Generator.CLASS_OPTIONS
            and not Clazz.objects.filter(Name=self.clazz.value).exists()
        ):
            return False
        background_list = Character_Generator.BACKGROUND_DICT.get("All")
        if (
            self.background.value != "All"
            and background_list is not None
            and self.background.value not in background_list
        ):
            return False
        if (
            self.race.value not in Character_Generator.RACE_OPTIONS
            and not Race.objects.filter(Name=self.race.value).exists()
        ):
            return False
        alignment_list = Character_Generator.ALIGNMENT_DICT.get("All")
        if (
            self.alignment.value != "All"
            and alignment_list is not None
            and self.alignment.value not in alignment_list
        ):
            return False
        return True


@dataclass
class Stat:
    """A stat element that tracks if it is checked as well as its proficiency"""

    value: int = 0
    repr: str = ""
    proficiency: int = 0
    checked: bool = False

    def sk_to_str(self):
        """Generates the string to display from the current state

        Returns:
            Stat: return self for chaining
        """
        val = self.value + self.proficiency
        pos = ""
        if self.value > 0:
            pos = "+"
        if self.value < 0:
            pos = "-"
        self.repr = f"{pos} {abs(val)}"
        return self

    def __post_init__(self):
        self.sk_to_str()


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
        proficiency=2,
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
            "strength": Stat(),
            "dexterity": Stat(),
            "constitution": Stat(),
            "intelligence": Stat(),
            "wisdom": Stat(),
            "charisma": Stat(),
            "acrobatics": Stat(),
            "animal_handling": Stat(),
            "arcana": Stat(),
            "athletics": Stat(),
            "deception": Stat(),
            "history": Stat(),
            "insight": Stat(),
            "intimidation": Stat(),
            "investigation": Stat(),
            "medicine": Stat(),
            "nature": Stat(),
            "perception": Stat(),
            "performance": Stat(),
            "persuasion": Stat(),
            "religion": Stat(),
            "sleight_of_hand": Stat(),
            "stealth": Stat(),
            "survival": Stat(),
        }
        if calculate is True:
            self.calculate()

    def update_proficiencies_from_dict(self, env: dict[str, Any]):
        """Takes POST request dict and updates checked boxes from it

        Args:
            env (dict[str, Any]): dictionary containing check boxes with same names as dict keys

        Returns:
            GeneratedCharacterOutputs: returns self for chaining
        """
        for stat in self.stats.values():
            stat.proficiency = 0
            stat.checked = False

        for ek in env.keys():
            sk = self.stats.get(ek)
            if sk is not None:
                sk.proficiency = self.proficiency.value
                sk.checked = True

        for k in self.stats.values():
            k.sk_to_str()

        return self

    def calculate(self):
        """Calculate all stat values

        Returns:
            GeneratedCharacterOutputs: returns self for chaining
        """
        self.stats[
            "mod_strength"
        ].value = Character_Generator.calculate_ability_modifier(self.strength)
        self.stats[
            "mod_dexterity"
        ].value = Character_Generator.calculate_ability_modifier(self.dexterity)
        self.stats[
            "mod_constitution"
        ].value = Character_Generator.calculate_ability_modifier(self.constitution)
        self.stats[
            "mod_intelligence"
        ].value = Character_Generator.calculate_ability_modifier(self.intelligence)
        self.stats["mod_wisdom"].value = Character_Generator.calculate_ability_modifier(
            self.wisdom
        )
        self.stats[
            "mod_charisma"
        ].value = Character_Generator.calculate_ability_modifier(self.charisma)

        self.stats["strength"].value = self.stats["mod_strength"].value
        self.stats["dexterity"].value = self.stats["mod_dexterity"].value
        self.stats["constitution"].value = self.stats["mod_constitution"].value
        self.stats["intelligence"].value = self.stats["mod_intelligence"].value
        self.stats["charisma"].value = self.stats["mod_charisma"].value
        self.stats["wisdom"].value = self.stats["mod_wisdom"].value
        self.stats["stat_initiative"].value = self.stats["mod_dexterity"].value
        self.stats["athletics"].value = self.stats["mod_strength"].value
        self.stats["acrobatics"].value = self.stats["mod_dexterity"].value
        self.stats["sleight_of_hand"].value = self.stats["mod_dexterity"].value
        self.stats["stealth"].value = self.stats["mod_dexterity"].value
        self.stats["animal_handling"].value = self.stats["mod_wisdom"].value
        self.stats["insight"].value = self.stats["mod_wisdom"].value
        self.stats["medicine"].value = self.stats["mod_wisdom"].value
        self.stats["perception"].value = self.stats["mod_wisdom"].value
        self.stats["survival"].value = self.stats["mod_wisdom"].value
        self.stats["deception"].value = self.stats["mod_charisma"].value
        self.stats["intimidation"].value = self.stats["mod_charisma"].value
        self.stats["performance"].value = self.stats["mod_charisma"].value
        self.stats["persuasion"].value = self.stats["mod_charisma"].value
        self.stats["religion"].value = self.stats["mod_intelligence"].value
        self.stats["arcana"].value = self.stats["mod_intelligence"].value
        self.stats["history"].value = self.stats["mod_intelligence"].value
        self.stats["nature"].value = self.stats["mod_intelligence"].value
        self.stats["investigation"].value = self.stats["mod_intelligence"].value

        for v in self.stats.values():
            v.sk_to_str()
            v.proficiency = self.proficiency.value

        return self
