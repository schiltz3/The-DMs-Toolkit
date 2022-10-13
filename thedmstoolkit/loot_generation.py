import random
from typing import Callable

from toolkit.models import Armor, GeneratedLoot, GenericItem, MagicItem, Weapon

Generator = Callable[[int, int], int]


class Loot_Generator:
    """Stores information for generating loot"""

    total_value_to_generate = 0.0
    total_value_generated = 0.0
    continue_generating = True
    currency = 0.0
    loot_type = "random"
    loot_level = 1
    generator_key = "random"
    armor_list: list[Armor] = []
    weapon_list: list[Weapon] = []
    gen_list: list[GenericItem] = []
    magic_list: list[MagicItem] = []
    LOOT_TYPE_DICT: dict[str, float] = {
        "Encounter": 1.0,
        "Treasure Chest": 10.0,
        "Hoard": 100.0,
        "Scraps": 0.1,
    }

    Generators: dict[str, Generator] = {}
    # Unlimited Generators have a minimum range of [1,max_int]
    UnlimitedGenerators: dict[str, Generator] = {"random": random.randint}
    Generators.update(UnlimitedGenerators)

    def check_value(self):
        """Checks if the current value has exceeded the intended loot generation"""
        if self.total_value_generated > self.total_value_to_generate:
            self.continue_generating = False

    def generate_loot_type(self):
        """Generate a random loot type"""
        loot_keys = list(Loot_Generator.LOOT_TYPE_DICT.keys())
        self.loot_type = loot_keys[
            Loot_Generator.Generators[self.generator_key](0, len(loot_keys) - 1)
        ]

    def generate_currency(self):
        """
        Generate a random amount of gold below the remaining value
        Then generates 0-100 silver
        Then generates 0-100 copper
        """
        local_currency = Loot_Generator.Generators[self.generator_key](
            0, self.total_value_to_generate - self.total_value_generated
        )
        local_currency += Loot_Generator.Generators[self.generator_key](1, 100) / 10
        local_currency += Loot_Generator.Generators[self.generator_key](1, 100) / 100
        self.currency += local_currency
        self.total_value_generated += local_currency
        self.check_value()

    def generate_weapon(self):
        """Get a list of all weapons from the database then pick a random one and add it to the list of things to add"""
        possible_weapons = list(Weapon.objects.all())
        new_weapon = possible_weapons[
            Loot_Generator.Generators[self.generator_key](0, len(possible_weapons) - 1)
        ]
        self.total_value_generated += new_weapon.Base_Value
        self.weapon_list.append(new_weapon)
        self.check_value()

    def generate_armor(self):
        """Get a list of all armor from the database then pick a random one and add it to the list of things to add"""
        possible_armor = list(Armor.objects.all())
        new_armor = possible_armor[
            Loot_Generator.Generators[self.generator_key](0, len(possible_armor) - 1)
        ]
        self.total_value_generated += new_armor.Base_Value
        self.armor_list.append(new_armor)
        self.check_value()

    def generate_generic_item(self):
        """Get a list of all random items from the database then pick a random one and add it to the list of things to add"""
        possible_items = list(GenericItem.objects.all())
        new_item = possible_items[
            Loot_Generator.Generators[self.generator_key](0, len(possible_items) - 1)
        ]
        self.total_value_generated += new_item.Base_Value
        self.gen_list.append(new_item)
        self.check_value()

    def generate_magical_item(self):
        """
        Get a list of all magic items from the database then pick a random one and add it to the list of things to add
        Ends Generation
        """
        possible_magic_items = list(MagicItem.objects.all())
        new_magic_item = possible_magic_items[
            Loot_Generator.Generators[self.generator_key](
                0, len(possible_magic_items) - 1
            )
        ]
        self.continue_generating = False
        self.total_value_generated += 1
        self.magic_list.append(new_magic_item)
        self.check_value()

    def generate_total_value(self):
        """
        Give a random integer that the minimum amount of value should be generated

        Equal to a random number between 1-10 and multiplied by the level and the treasure type
        """

        self.total_value_to_generate = (
            (Loot_Generator.Generators[self.generator_key](1, 10))
            * self.loot_level
            * Loot_Generator.LOOT_TYPE_DICT[self.loot_type]
        )

    GENERATOR_DICT = {
        "Currency": generate_currency,
        "Armor": generate_armor,
        "Weapon": generate_weapon,
        "Generic": generate_generic_item,
        "Magic": generate_magical_item,
    }

    def generate_random(self):
        """Choose which item to randomly generate"""
        gen_keys = list(Loot_Generator.GENERATOR_DICT.keys())
        to_generate = Loot_Generator.Generators[self.generator_key](
            0, len(gen_keys) - 1
        )
        Loot_Generator.GENERATOR_DICT[gen_keys[to_generate]](self)

    def generate_loot(
        self,
        generator_key="random",
        level=1,
        approximate_total_value=0,
        input_loot_type="random",
    ):
        """
        Overall Function - generates all the loot types

        Args:
            generator_key (str, optional): which generator to use choose from keys on Generators.keys. Defaults to "random".
            level (int, optional): average level of the party. Defaults to 1.
            approximate_total_value (double, optional): how much value should be generated is 0 only temporarily on default. Defaults to 0.
            input_loot_type (str, optional): What kind of loot choose from keys on LOOT_TYPE_DICT. Defaults to "random".

        Raises:
            ValueError: If generator key is not contained in the dictionary
            ValueError: If a non int is passed as a level
            ValueError: If the level isn't possible to get in D&D
            ValueError: If tne total value isn't an integer
            ValueError: If the total value is below zero
            ValueError: If the loot type is not random or a valid loot type key
        Returns:
            GeneratedLoot: an item to put in the GeneratedLoot model
        """

        if not generator_key in Loot_Generator.Generators.keys():
            raise ValueError("Illegal generator type")
        if not type(level) is int:
            raise ValueError("Not a valid Level")
        if not 0 < level <= 21:
            raise ValueError("Illegal Level")
        if not type(approximate_total_value) is int:
            raise ValueError("Not a valid Level")
        if approximate_total_value < 0:
            raise ValueError("Illegal Total Value")

        if (
            input_loot_type is not "random"
            or input_loot_type not in Loot_Generator.LOOT_TYPE_DICT
        ):
            raise ValueError("Illegal Loot Type")
        self.generator_key = generator_key
        if input_loot_type is "random":
            self.generate_loot_type()
        self.loot_level = level
        if approximate_total_value != 0:
            self.generate_total_value()
        else:
            self.total_value_to_generate = approximate_total_value

        while self.continue_generating:
            self.generate_random()

        current_loot = GeneratedLoot(
            Loot_Type=self.loot_type,
            Total_Value=self.total_value_generated,
            Money=self.currency,
        )
        current_loot.save()
        for armor in self.armor_list:
            current_loot.Armors.add(armor)
        for weapon in self.weapon_list:
            current_loot.Weapons.add(weapon)
        for item in self.gen_list:
            current_loot.Generic_Items.add(item)
        for magic_item in self.magic_list:
            current_loot.Magical_Items.add(magic_item)
        return current_loot
