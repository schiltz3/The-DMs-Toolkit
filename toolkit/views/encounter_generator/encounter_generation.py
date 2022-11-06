import random
from typing import Callable, Optional, Union

from toolkit.models import Monster, Tag
from toolkit.views.loot_generator.loot_generation import Loot_Generator

Generator = Callable[[int, int], int]


class Encounter_Generator:
    """_summary_

    Raises:
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        ValueError: _description_
        RuntimeError: _description_
        ValueError: _description_
        ValueError: _description_

    Returns:
        _type_: _description_
    """

    ENCOUNTER_TYPE_LIST = [
        "Horde",
        "Skirmish",
        "Average Encounter",
        "Challenge",
        "Minor Boss",
        "Major Boss",
    ]
    Generators: dict[str, Generator] = {"Random": random.randint}

    def __init__(self):
        """Initiates Values"""
        self.gen = Loot_Generator()
        self.average_party_level = 1
        self.tags: list[Tag] = []
        self.average_cr = 0
        self.monster_list: list[Monster] = []
        self.encounter_type = "Average Encounter"
        self.dropped_loot = None
        self.highest_loot_modifier = 0
        self.generator_key = "Random"

    def get_tags(self):
        """Get Current Tags

        Returns:
            List: List of Tags
        """
        return self.tags

    def add_tag(self, tag):
        """_summary_

        Args:
            tag (Tag|string): accepts either a tag object or a string that is the same as the name of a tag

        Raises:
            ValueError: If the tag is a string and no matching tag is in the database
            ValueError: If the tag is a tag object and not in the database
            ValueError: If the tag is not a string or tag object
        """
        check = list(Tag.objects.all())
        if type(tag) is str:
            valid = False
            for x in check:
                if x.Name == tag:
                    valid = True
                    added_tag = x
            if not valid:
                raise ValueError("Not a Valid Tag")
        elif type(tag) is Tag:
            added_tag = tag
            if added_tag not in check:
                raise ValueError("Not a Valid Tag")
        else:
            raise ValueError("Invalid Tag")
        self.tags.append(added_tag)

    def remove_tag(self, tag):
        """Removes a tag from the list

        Args:
            tag (Tag|string): accepts either a tag object or a string that is the same as the name of a tag

        Raises:
            ValueError: If the tag is a string and no matching tag is in the database
            ValueError: If the tag is a tag object and not in the database
            ValueError: If the tag is not a string or tag object
        """
        check = list(Tag.objects.all())
        if type(tag) is str:
            valid = False

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
        """returns the average cr of the encounter

        Returns:
           Float: Average cr of the generated monsters
        """
        return self.average_cr

    def get_average_level(self):
        """returns the average level of the players

        Returns:
           Float: Average level of the players
        """
        return self.average_party_level

    def change_average_level(self, new_level):
        """Adjust the average level

        Args:
            new_level (int or float): New average level

        Raises:
            ValueError: If new_level is not a float or int
            ValueError: If new level is not possible to get in dnd
        """
        if type(new_level) is not float and type(new_level) is not int:
            raise ValueError("Not a float level")
        if not 1 <= new_level <= 21:
            raise ValueError("Not a valid level")
        self.average_party_level = new_level

    def get_monster_list(self):
        """Returns the list of monsters generated

        Returns:
            List: a list of all monsters generated so far
        """
        return self.monster_list

    def get_encounter_type(self):
        """Returns the type of encounter

        Returns:
            String: type of encounter
        """
        return self.encounter_type

    def set_encounter_type(self, encounter_type):
        """Change the encounter type

        Args:
            encounter_type (String): One of the accepted encounter types

        Raises:
            ValueError: If encounter_type is not a valid encounter type
        """
        if encounter_type not in self.ENCOUNTER_TYPE_LIST:
            raise ValueError("Not a valid encounter type")
        self.encounter_type = encounter_type

    def get_loot(self):
        """Returns the loot

        Returns:
            Dictionary: The standard dictionary returned by the generate function from the loot generator
        """
        return self.dropped_loot

    def get_loot_modifier(self):
        """Return the amount the monsters currently modify the loot generated
        Loot Modifier currently not used

        Returns:
            float: modifier for loot dropped
        """
        return self.highest_loot_modifier

    def calculate_average_cr(self):
        """calculates and updates the average cr, only used internally"""
        cr_sum = 0.0
        for x in self.monster_list:
            cr_sum += x.Challenge_Rating
        self.average_cr = cr_sum / len(self.monster_list)

    def generate_loot(self):
        """Generates some loot based on the encounter"""
        if self.encounter_type == "Major Boss":
            loot = self.gen.generate_loot(
                generator_key=self.generator_key,
                level=int(self.average_party_level),
                input_loot_type="Horde",
            )
        elif self.encounter_type == "Minor Boss":
            loot = self.gen.generate_loot(
                generator_key=self.generator_key,
                level=int(self.average_party_level),
                input_loot_type="Treasure Chest",
            )
        else:
            loot = self.gen.generate_loot(
                generator_key=self.generator_key,
                level=int(self.average_party_level),
                input_loot_type="Encounter",
            )
        self.dropped_loot = loot

    def generate_monster(self):
        """Main function of the method, generates a monster randomly from the databases and adds it to the list

        Raises:
            RuntimeError: If there are no monsters suitable to be generated
        """

        if self.encounter_type == "Average Encounter":
            monster_possibilities = Monster.objects.filter(
                Challenge_Rating__lte=(self.average_party_level + 1)
            )

            monster_possibilities = monster_possibilities.filter(
                Challenge_Rating__gte=(
                    (self.average_party_level + (self.average_party_level - 1)) / 2
                )
            )

        elif self.encounter_type == "Horde":
            monster_possibilities = Monster.objects.filter(
                Challenge_Rating__lte=(
                    (self.average_party_level + (self.average_party_level - 2)) / 3
                )
            )
            monster_possibilities = monster_possibilities.filter(
                Challenge_Rating__gte=(
                    (self.average_party_level + (self.average_party_level - 2)) / 4
                )
            )
        elif self.encounter_type == "Skirmish":
            monster_possibilities = Monster.objects.filter(
                Challenge_Rating__lte=self.average_party_level
            )
            monster_possibilities = monster_possibilities.filter(
                Challenge_Rating__gte=(
                    (self.average_party_level + (self.average_party_level - 2)) / 2
                )
            )
        elif self.encounter_type == "Challenge":
            if 10 > self.average_party_level > 1:
                monster_possibilities = monster_possibilities = Monster.objects.filter(
                    Challenge_Rating__lte=(
                        (self.average_party_level + (self.average_party_level + 3)) / 2
                    )
                )
            elif self.average_party_level >= 10:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating__lte=(
                        self.average_party_level + (self.average_party_level / 3)
                    )
                )
            else:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating__lte=self.average_party_level
                )
            monster_possibilities = monster_possibilities.filter(
                Challenge_Rating__gte=self.average_party_level - 1
            )

        elif self.encounter_type == "Minor Boss":
            if 10 > self.average_party_level > 3:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating__lte=(
                        (self.average_party_level + (self.average_party_level + 3)) / 2
                    )
                )
            elif self.average_party_level >= 10:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating__lte=(
                        self.average_party_level + (self.average_party_level / 3) + 1
                    )
                )
            else:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating__lte=self.average_party_level + 2
                )
            monster_possibilities = monster_possibilities.filter(
                Challenge_Rating__gt=self.average_party_level
            )

        elif self.encounter_type == "Major Boss":
            if 10 > self.average_party_level < 4:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating__lte=(
                        (
                            self.average_party_level
                            + ((self.average_party_level + 3) / 2)
                        )
                    )
                )
            elif self.average_party_level > 10:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating__lte=(
                        self.average_party_level + (self.average_party_level / 3) + 1
                    )
                )
            else:
                monster_possibilities = Monster.objects.filter(
                    Challenge_Rating__lte=self.average_party_level + 2
                )
                monster_possibilities = monster_possibilities.filter(
                    Challenge_Rating__gt=self.average_party_level
                )

        for x in self.tags:
            monster_possibilities = monster_possibilities.filter(Creature_Tags=x)
        if len(monster_possibilities) > 1:
            monster_possibilities = list(monster_possibilities)
            toAdd = monster_possibilities[
                self.Generators[self.generator_key](0, (len(monster_possibilities) - 1))
            ]

        elif len(monster_possibilities) == 1:
            toAdd = monster_possibilities[0]
        else:
            raise RuntimeError("No monsters with those tags at your levels")
        if (
            toAdd.Gold_Modifier is not None
            and toAdd.Gold_Modifier > self.highest_loot_modifier
        ):
            self.highest_loot_modifier = toAdd.Gold_Modifier
        self.monster_list.append(toAdd)
        self.calculate_average_cr()

    def generate_encounter(
        self,
        average_level=1,
        encounter_type="Average Encounter",
        tags=None,
        generator_key="Random",
        loot_generate=False,
    ):
        """Outwards facing component of the generate encounter, generates a somewhat random amount of monsters

        Args:
            average_level (int or float, optional): Average Level of the party. Defaults to 1.
            encounter_type (str, optional): Type of encounter to be generated. Defaults to "Average Encounter".
            tags (List of Tags or strings, optional): A list of all tags to be included, tags stack to further limit not expand.
                Defaults to None.
            generator_key (str, optional): Generator Type. Defaults to "Random".
            loot_generate (bool, optional): Boolean generate loot or not. Defaults to False.

        Raises:
            ValueError: Generator Key is not valid
            ValueError: Loot Generate is not true or false
        """
        monster_count = 0
        if tags is None:
            tags = []
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
        elif self.encounter_type == "Skirmish":
            monster_count = self.Generators[self.generator_key](1, 3)
        elif self.encounter_type == "Challenge":
            monster_count = self.Generators[self.generator_key](1, 3)
        else:
            monster_count = 1
        for x in range(monster_count):
            self.generate_monster()
        if loot_generate:
            self.generate_loot()
