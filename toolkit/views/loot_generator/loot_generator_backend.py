import random
from typing import Callable

from toolkit.models import Armor, GeneratedLoot, GenericItem, MagicItem, Weapon

Generator = Callable[[int, int], int]


class Loot_Generator:
    """Stores information for generating loot"""

    LOOT_TYPE_DICT: dict[str, float] = {
        "Encounter": 1.0,
        "Treasure Chest": 10.0,
        "Hoard": 100.0,
        "Scraps": 0.1,
    }

    def __init__(self):
        """Sets"""
        self.min_value_to_generate = 0.0
        self.total_value_generated = 0.0
        self.continue_generating = True
        self.currency = 0.0
        self.loot_type = "Random"
        self.loot_level = 1
        self.generator_key = "Random"
        self.armor_list: list[Armor] = []
        self.weapon_list: list[Weapon] = []
        self.gen_list: list[GenericItem] = []
        self.magic_list: list[MagicItem] = []
        self.Generators: dict[str, Generator] = {}
        # Unlimited Generators have a minimum range of [1,max_int]
        self.UnlimitedGenerators: dict[str, Generator] = {"Random": random.randint}
        self.Generators.update(self.UnlimitedGenerators)

    def get_all_random_generators(self):
        """
        Gives the list of random generator keys
        Returns:
            List: a list of all generator keys
        """
        return list(self.Generators.keys())

    def check_value(self):
        """Checks if the current value has exceeded the intended loot generation"""
        if self.total_value_generated > self.min_value_to_generate:
            self.continue_generating = False

    def generate_loot_type(self):
        """Generate a random loot type"""
        loot_keys = list(Loot_Generator.LOOT_TYPE_DICT.keys())
        self.loot_type = loot_keys[
            self.Generators[self.generator_key](0, len(loot_keys) - 1)
        ]

    def generate_currency(self):
        """
        Generate a random amount of gold below the remaining value
        Then generates 0-100 silver
        Then generates 0-100 copper
        """
        local_currency = self.Generators[self.generator_key](
            0, int(self.min_value_to_generate - self.total_value_generated)
        )
        local_currency += self.Generators[self.generator_key](1, 100) / 10
        local_currency += self.Generators[self.generator_key](1, 100) / 100
        self.currency += local_currency
        self.total_value_generated += local_currency

    def generate_weapon(self):
        """Get a list of all weapons from the database then pick a random one and add it to the list of things to add"""
        possible_weapons = list(Weapon.objects.all())
        if len(possible_weapons) == 0:
            raise ValueError("Failed to retrieve weapons from database")
        new_weapon = possible_weapons[
            self.Generators[self.generator_key](0, len(possible_weapons) - 1)
        ]
        self.total_value_generated += new_weapon.Base_Value
        self.weapon_list.append(new_weapon)

    def generate_armor(self):
        """Get a list of all armor from the database then pick a random one and add it to the list of things to add"""
        possible_armor = list(Armor.objects.all())
        if len(possible_armor) == 0:
            raise ValueError("Failed to retrieve armor from database")
        new_armor = possible_armor[
            self.Generators[self.generator_key](0, len(possible_armor) - 1)
        ]
        self.total_value_generated += new_armor.Base_Value
        self.armor_list.append(new_armor)

    def generate_generic_item(self):
        """Get a list of all random items from the database then pick a random one and add it to the list of things to add"""
        possible_items = list(GenericItem.objects.all())
        if len(possible_items) == 0:
            raise ValueError("Failed to retrieve items from database")
        new_item = possible_items[
            self.Generators[self.generator_key](0, len(possible_items) - 1)
        ]
        self.total_value_generated += new_item.Base_Value
        self.gen_list.append(new_item)

    def generate_magical_item(self):
        """
        Get a list of all magic items from the database then pick a random one and add it to the list of things to add
        Ends Generation
        """
        possible_magic_items = list(MagicItem.objects.all())
        if len(possible_magic_items) == 0:
            raise ValueError("Failed to retrieve magical items from database")
        new_magic_item = possible_magic_items[
            self.Generators[self.generator_key](0, len(possible_magic_items) - 1)
        ]
        self.continue_generating = False
        self.total_value_generated += 1
        self.magic_list.append(new_magic_item)

    def generate_total_value(self):
        """
        Give a random integer that the minimum amount of value should be generated

        Equal to a random number between 1-10 and multiplied by the level and the treasure type
        """

        self.min_value_to_generate = (
            (self.Generators[self.generator_key](1, 10))
            * self.loot_level
            * Loot_Generator.LOOT_TYPE_DICT[self.loot_type]
        )

    LOOT_GENERATOR_DICT = {
        "Currency": generate_currency,
        "Armor": generate_armor,
        "Weapon": generate_weapon,
        "Generic": generate_generic_item,
        "Magic": generate_magical_item,
    }

    def generate_random(self):
        """Choose which item to randomly generate"""
        gen_keys = list(Loot_Generator.LOOT_GENERATOR_DICT.keys())
        to_generate = self.Generators[self.generator_key](0, len(gen_keys) - 1)
        Loot_Generator.LOOT_GENERATOR_DICT[gen_keys[to_generate]](self)

    def generate_loot(
        self,
        generator_key="Random",
        level=1,
        approximate_total_value=0,
        input_loot_type="Random",
    ):
        """
        Overall Function - generates all the loot types

        Args:
            generator_key (str, optional): which generator to use choose from keys on Generators.keys.
            Generate key is static for every generation type. Defaults to "random".
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
            loot_dict: a dictionary containing the loot object and all item lists to add
        """

        if generator_key not in self.Generators:
            raise ValueError("Illegal generator type")
        if not type(level) is int:
            raise ValueError("Not a valid Level")
        if not 0 < level <= 21:
            raise ValueError("Illegal Level")
        if not type(approximate_total_value) is int:
            raise ValueError("Not a valid total")
        if approximate_total_value < 0:
            raise ValueError("Illegal Total Value")

        if (
            input_loot_type != "Random"
            and input_loot_type not in Loot_Generator.LOOT_TYPE_DICT
        ):
            raise ValueError("Illegal Loot Type")

        self.generator_key = generator_key
        self.loot_level = level

        if input_loot_type == "Random":
            self.generate_loot_type()
        else:
            self.loot_type = input_loot_type
        if approximate_total_value == 0:
            self.generate_total_value()
        else:
            self.min_value_to_generate = approximate_total_value

        while self.continue_generating:
            self.generate_random()
            self.check_value()

        current_loot = GeneratedLoot(
            Loot_Type=self.loot_type,
            Total_Value=self.total_value_generated,
            Money=self.currency,
        )
        loot_dict = {
            "loot_object": current_loot,
            "armor": self.armor_list,
            "weapons": self.weapon_list,
            "general": self.gen_list,
            "magic": self.magic_list,
        }
        return loot_dict
