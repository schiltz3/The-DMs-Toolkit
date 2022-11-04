import random
from typing import Callable, Optional, Union

from toolkit.models import Monster, Tag
from toolkit.views.loot_generator.loot_generation import Loot_Generator

Generator = Callable[[int, int], int]


class Encounter_Generator:
    ENCOUNTER_TYPE_LIST = [
        "Horde",
        "Scrimish",
        "Average Encounter",
        "Challenge",
        "Minor Boss",
        "Major Boss",
    ]
    Generators: dict[str, Generator] = {}
    UnlimitedGenerators: dict[str, Generator] = {"Random": random.randint}

    def __init__(self):
        self.average_party_level = 1
        self.tags = None
        if self.tags is None:
            self.tags = []
        self.average_cr = 0
        self.monster_list = None
        if self.monster_list is None:
            self.monster_list = []
        self.encounter_type = "Average Encounter"
        self.dropped_loot = None
        self.highest_loot_modifier = 0
        self.generator_key = "Random"

    def get_tags(self):
        return self.tags

    def add_tag(self, tag):
        if type(tag) is str:
            valid = False
            check = list(Tag.objects.all())
            for x in check:
                if x.Name == tag:
                    valid = True
                    added_tag = x
            if not valid:
                raise ValueError("Not a Valid Tag")
        elif type(tag) is Tag:
            added_tag = tag
            if tag not in check:
                raise ValueError("Not a Valid Tag")
        else:
            raise ValueError("Invalid Tag")
        self.tags.append(added_tag)

    def remove_tag(self, tag):
        if type(tag) is str:
            valid = False
            check = list(Tag.objects.all())
            for x in check:
                if x.Name == tag:
                    valid = True
                    removed_tag = x
            if not valid:
                raise ValueError("Not a Valid Tag")
        elif type(tag) is Tag:
            removed_tag = tag
            if tag not in check:
                raise ValueError("Not a Valid Tag")
        else:
            raise ValueError("Invalid Tag")
        self.tags.remove(removed_tag)

    def get_average_cr(self):
        return self.average_cr

    def get_average_level(self):
        return self.average_party_level

    def change_average_level(self, new_level):
        if type(new_level) is not float:
            raise ValueError("Not a float level")
        if 1 > new_level > 21:
            raise ValueError("Not a valid level")
        self.average_party_level = new_level

    def get_monster_list(self):
        return self.monster_list

    def get_encounter_type(self):
        return self.encounter_type

    def set_encounter_type(self, encounter_type):
        if encounter_type not in self.ENCOUNTER_TYPE_LIST:
            raise ValueError("Not a valid encounter type")

    def get_loot(self):
        return self.dropped_loot

    def get_loot_modifier(self):
        return self.highest_loot_modifier

    def calculate_average_cr(self):
        sum = 0
        for x in self.monster_list:
            sum += x.Challenge_Rating
        self.average_cr = sum / len(self.monster_list)

    def generate_loot(self):
        generator = Loot_Generator()
        loot = generator.generate_loot(
            self, self.generator_key, int(self.average_party_level)
        )
        self.dropped_loot = loot

    def generate_monster(self):
        if self.encounter_type == "Average Encounter":
            monster_possibilities = Monster.objects.filter(
                Challenge_Rating <= self.average_party_level + 1
            )
            monster_possibilities.filter(
                Challenge_Rating
                >= ((self.average_party_level + (self.average_party_level - 1)) / 2)
            )
        elif self.encounter_type == "Horde":
            monster_possibilities = Monster.objects.filter(
                Challenge_Rating
                <= ((self.average_party_level + (self.average_party_level - 2)) / 3)
            )
            monster_possibilities.filter(
                Challenge_Rating
                >= ((self.average_party_level + (self.average_party_level - 2)) / 4)
            )
        elif self.encounter_type == "Scrimish":
            monster_possibilities = Monster.objects.filter(
                Challenge_Rating <= self.average_party_level
            )
            monster_possibilities.filter(
                Challenge_Rating
                >= ((self.average_party_level + (self.average_party_level - 2)) / 2)
            )
        elif self.encounter_type == "Challenge":
            if 10 > self.average_party_level > 1:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating
                    <= ((self.average_party_level + (self.average_party_level + 3)) / 2)
                )
            elif self.average_party_level >= 10:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating
                    <= (self.average_party_level + (self.average_party_level / 3))
                )
            else:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating <= self.average_party_level
                )
            monster_possibilities.filter(
                Challenge_Rating >= self.average_party_level - 1
            )

        elif self.encounter_type == "Minor Boss":
            if 10 > self.average_party_level > 3:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating
                    <= ((self.average_party_level + (self.average_party_level + 3)) / 2)
                )
            elif self.average_party_level >= 10:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating
                    <= (self.average_party_level + (self.average_party_level / 3) + 1)
                )
            else:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating <= self.average_party_level + 2
                )
            monster_possibilities.filter(Challenge_Rating > self.average_party_level)

        elif self.encounter_type == "Major Boss":
            if 10 > self.average_party_level < 4:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating
                    <= (
                        (
                            self.average_party_level
                            + ((self.average_party_level + 3) / 2)
                        )
                    )
                )
            elif self.average_party_level > 10:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating
                    <= (self.average_party_level + (self.average_party_level / 3) + 1)
                )
            else:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating <= self.average_party_level + 2
                )
        monster_possibilities.filter(Challenge_Rating > self.average_party_level)

        for x in self.tags:
            monster_possibilities.filter(Creature_Tags=x)
        if monster_possibilities.exists:
            monster_possibilities = list(monster_possibilities)
            self.monster_list.append(
                monster_possibilities[
                    self.Generators[self.generator_key](
                        0, (len(monster_possibilities) - 1)
                    )
                ]
            )
            self.calculate_average_cr()
        else:
            raise RuntimeError("No monsters with those tags at your levels")

    def generate_encounter(
        self,
        average_level=1,
        encounter_type="Average Encounter",
        tags=[],
        generator_key="Random",
        loot_generate=False,
    ):
        monster_count = 0
        if generator_key not in self.Generators:
            raise ValueError("Illegal Value")
        if type(loot_generate) is not bool:
            raise ValueError("Illegal loot generate value")
        self.change_average_level(average_level)
        self.set_encounter_type(encounter_type)
        for x in tags:
            self.add_tag(x)
        if self.encounter_type == "Average Encounter":
            monster_count = self.Generators[self.generator_key](1, 4)
        elif self.encounter_type == "Horde":
            monster_count = self.Generators[self.generator_key](5, 10)
        elif self.encounter_type == "Scrimish":
            monster_count = self.Generators[self.generator_key](1, 3)
        elif self.encounter_type == "Challenge":
            monster_count = self.Generators[self.generator_key](1, 3)
        else:
            monster_count = 1
        for x in range(monster_count):
            self.generate_monster()
