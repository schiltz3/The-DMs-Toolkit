import random
from math import ceil
from typing import Callable, Optional, Union

Generator = Callable[[int, int], int]


class Character_Generator:
    """
    Contains all the lists and Dictionaries
    for the various character generation methods
    """

    RACE_DICT: dict[str, list] = {
        "Rare": [
            "Aasimar",
            "Animal Hybrid",
            "Aarakocra",
            "Centaur",
            "Changeling",
            "Dragonborn",
            "Kalashtar",
            "Elephantine",
            "Fairy",
            "Firbolg",
            "Genasi",
            "Geth",
            "Goliath",
            "Harengon",
            "Hexed Lineage",
            "Kenku",
            "Leonine",
            "Minotaur",
            "Owlin",
            "Reborn Lineage",
            "Satyr",
            "Yuan-Ti",
            "Shifter",
            "Tabaxi",
            "Tiefling",
            "Triton",
            "Tortle",
            "Vedalken",
            "Warforged",
            "Locathah",
        ],
        "Monster": ["Bugbear", "Goblin", "Hobgoblin", "Kobold", "Lizardfolk", "Orc"],
        "Common": [
            "Dwarf",
            "Elf",
            "Gnome",
            "Half-Elf",
            "Half-Orc",
            "Halfling",
            "Human",
        ],
        "All": [
            "Aasimar",
            "Animal Hybrid",
            "Aarakocra",
            "Centaur",
            "Changeling",
            "Dragonborn",
            "Kalashtar",
            "Elephantine",
            "Fairy",
            "Firbolg",
            "Genasi",
            "Geth",
            "Goliath",
            "Harengon",
            "Hexed Lineage",
            "Kenku",
            "Leonine",
            "Minotaur",
            "Owlin",
            "Reborn Lineage",
            "Satyr",
            "Yuan-Ti",
            "Shifter",
            "Tabaxi",
            "Tiefling",
            "Triton",
            "Tortle",
            "Vedalken",
            "Warforged",
            "Locathah",
            "Bugbear",
            "Goblin",
            "Hobgoblin",
            "Kobold",
            "Lizardfolk",
            "Orc",
            "Dwarf",
            "Elf",
            "Gnome",
            "Half-Elf",
            "Half-Orc",
            "Halfling",
            "Human",
        ],
    }
    CLASS_DICT: dict[str, list] = {
        "Martial": ["Fighter", "Monk", "Ranger", "Rogue"],
        "Divine": ["Cleric", "Paladin", "Warlock"],
        "Magic": ["Artificer", "Bard", "Druid", "Sorcerer", "Wizard"],
        "All": [
            "Fighter",
            "Monk",
            "Ranger",
            "Rogue",
            "Cleric",
            "Paladin",
            "Warlock",
            "Artificer",
            "Bard",
            "Druid",
            "Sorcerer",
            "Wizard",
        ],
    }
    ALIGNMENT_DICT: dict[str, list] = {
        "Good": ["Lawful Good", "Neutral Good", "Chaotic Good"],
        "Neutral": ["Lawful Neutral", "True Neutral", "Chaotic Neutral"],
        "Evil": ["Lawful Evil", "Neutral Evil", "Chaotic Evil"],
        "All": [
            "Lawful Good",
            "Neutral Good",
            "Chaotic Good",
            "Lawful Neutral",
            "True Neutral",
            "Chaotic Neutral",
            "Lawful Evil",
            "Neutral Evil",
            "Chaotic Evil",
        ],
    }
    BACKGROUND_DICT = {
        "All": [
            "Acolyte",
            "Athlete",
            "Barbarian Tribe Member",
            "Charlatan",
            "City Watch",
            "Criminal",
            "Clan Crafter",
            "Entertainer",
            "Faction Agent",
            "Far Traveler",
            "Fisher",
            "Folk Hero",
            "Gladiator",
            "Hermit",
            "Knight",
            "Noble",
            "Outlander",
            "Pirate",
            "Sage",
            "Sailor",
            "Soldier",
            "Urchin",
        ]
    }
    GENERATOR_LIST: list[str] = ["Stats", "Race", "Class", "Alignment", "Background"]
    STANDARD_ARRAY: list[int] = [15, 14, 13, 12, 10, 8]

    def __init__(self):

        self.generators: dict[str, Generator] = {}
        # Unlimited Generators have a minimum range of [1,max_int]
        self.UnlimitedGenerators: dict[str, Generator] = {"Random": random.randint}
        # Limited Generators have a max range of [1,20], and therefore are not suitable for use in generating race, class, etc
        self.LimitedGenerators: dict[str, Generator] = {"3D6": self.three_d_six}
        self.generators.update(self.LimitedGenerators)
        self.generators.update(self.UnlimitedGenerators)

    @staticmethod
    def three_d_six(_low, _high) -> int:
        """Returns the total od 3d6

        Args:
            _low (_type_): Ignored
            _high (_type_): Ignored

        Returns:
            int: Returns the total of 3d6
        """
        return random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6)

    @staticmethod
    def get_proficiency_modifier(level):
        """_summary_

        Args:
            level (Integer): Character Level

        Raises:
            RuntimeError: Not a integer
            ValueError: Not a valid level

        Returns:
            Proficiency value: the value to add to proficiencies based on level given
        """
        if type(level) is not int:
            raise RuntimeError("Level is not an integer")
        if not 0 < level <= 30:
            raise ValueError("Illegal Level")
        return ceil(level / 4) + 1

    @staticmethod
    def calculate_ability_modifier(stat: int) -> int:
        """Takes a stat and returns the ability modifier as a string

        Args:
            stat (int): the stat

        Returns:
            str: ability modifier string
        """
        if type(stat) is not int:
            raise RuntimeError("Stat is not an integer")
        if not 0 <= stat <= 20:
            raise ValueError("Illegal Level")
        return (stat - 10) // 2
        return str(value) if value < 0 else f"+{value}"

    @staticmethod
    def get_all_generators():
        """
        Gives the list of generator keys
        Returns:
            List: a list of all generator keys
        """
        return Character_Generator.GENERATOR_LIST

    def get_all_random_generators(self):
        """
        Gives the list of random generator keys
        Returns:
            List: a list of all generator keys
        """
        return list(self.generators.keys())

    @staticmethod
    def get_limited_generators():
        """
        Gives the list of limited generator keys
        Returns:
            List: a list of all limited generator keys
        """
        return Character_Generator.LimitedGenerators.keys()

    @staticmethod
    def get_unlimited_generators():
        """
        Gives the list of unlimited generator keys
        Returns:
            List: a list of all unlimited generator keys
        """
        return Character_Generator.UnlimitedGenerators.keys()

    def generate_stat_list(self, generator_key: str):
        """Returns the Stat List needed because the dictionary is in str:function

        Args:
            generator_key (str): key required to specify which randomizer you want

        Raises:
            RuntimeError: If the key provided is the wrong type

        Returns:
            StatList (List): List of stat values
        """
        if generator_key not in self.generators:
            raise RuntimeError("Generator does not exist")
        i = 0
        stat_list: list[int] = []
        while i < 6:
            stat_list.insert(i, self.generators[generator_key](1, 18))
            i = i + 1
        return stat_list

    def generate_race(self, race_list: list[str], generator_key: str) -> str:
        """
        Generates a race from the provided list
        Args:
            RaceList (list): The list chosen from the dictionary
            generator_key (str): key required to specify which randomizer you want

        Raises:
            RuntimeError: If the key provided is the wrong type
            RuntimeError: If there is an unauthorized item in the passed list

        Returns:
            String: Race
        """
        if generator_key not in self.generators:
            raise RuntimeError("Generator does not exist")
        for x in race_list:
            if x not in Character_Generator.RACE_DICT["All"]:
                raise RuntimeError("Invalid List")
        race: str = race_list[self.generators[generator_key](0, len(race_list) - 1)]
        return race

    def generate_class(self, class_list: list[str], generator_key: str) -> str:
        """
        Returns a random class from the provided list
        Args:
            class_list (List): The list chosen from the Class dictionary
            generator_key (str): key required to specify which randomizer you want

        Raises:
            RuntimeError: If the key provided is the wrong type
            RuntimeError: If there is an unauthorized item in the passed list

        Returns:
            String: the random class
        """
        if generator_key not in self.generators:
            raise RuntimeError("Generator does not exist")
        for x in class_list:
            if x not in Character_Generator.CLASS_DICT["All"]:
                raise RuntimeError("Invalid List")
        clazz: str = class_list[self.generators[generator_key](0, len(class_list) - 1)]
        return clazz

    def generate_alignment(self, alignment_list: list[str], generator_key: str) -> str:
        """
            Returns a random alignment from the provided list
        Args:
            AlignmentList (List): List of alignments from alignment dictionary
            generator_key (str): key required to specify which randomizer you want

        Raises:
            RuntimeError: If the key provided is the wrong type
            RuntimeError: If there is an unauthorized item in the passed list

        Returns:
            String: Alignment
        """
        if generator_key not in self.generators:
            raise RuntimeError("Generator does not exist")
        for x in alignment_list:
            if x not in Character_Generator.ALIGNMENT_DICT["All"]:
                raise RuntimeError("Invalid List")
        alignment = alignment_list[
            self.generators[generator_key](0, len(alignment_list) - 1)
        ]
        return alignment

    def generate_background(
        self, background_list: list[str], generator_key: str
    ) -> str:
        """
            Generate a random background
        Args:
            background_list (str): background
            generator_key (str): key required to specify which randomizer you want
        Raises:
            RuntimeError: If the key provided is the wrong type
            RuntimeError: If there is an unauthorized item in the passed list

        Returns:
            String: Background
        """
        if generator_key not in self.generators:
            raise RuntimeError("Generator does not exist")
        for x in background_list:
            if x not in Character_Generator.BACKGROUND_DICT["All"]:
                raise RuntimeError("Invalid List")
        return background_list[
            self.generators[generator_key](0, len(background_list) - 1)
        ]

    def generate(
        self,
        generations_list: Optional[list[str]] = None,
        stat_generator_key: Optional[str] = None,
        race_key="All",
        class_key="All",
        alignment_key="All",
        background_key="All",
        generator_key="Random",
        stat_list: Optional[list[int]] = None,
    ) -> dict[str, Union[list[int], str]]:
        """Given generator parameters, return a dictionary of character characteristics

        Args:
            generations_list (str, optional): A list of the various generations to do. Defaults to "All".
            stat_generator_key (Optional[str], optional): A generator name from limited_generators(). Defaults to None.
            race_key (str, optional): A race category, from the RACE_DICT. Defaults to "All".
            class_key (str, optional): A class category from the CLASS_DICT. Defaults to "All".
            alignment_key (str, optional): A alignment category from the ALIGNMENT_DICT. Defaults to "All".
            stat_list (list[int], optional): A list of 6 numbers between 1 and 20 to use as stats. Defaults to None.

        Raises:
            ValueError: _description_
            RuntimeError: Not all numbers are in the passed stat array are valid

        Returns:
            dict[str, list[int] | str]: Generated Characteristics
        """

        if type(stat_list) is not list and stat_list is not None:
            raise ValueError("Improper Argument in stat list")
        if type(stat_list) is list:
            if len(stat_list) != 6:
                raise ValueError("Stat list length must be 6")

            for i in stat_list:
                if type(i) != int:
                    raise RuntimeError("Not all numbers in Stat array are integers")
                if not 0 < i <= 18:
                    raise RuntimeError(
                        "There is an invalid number in the array, please use 1-18"
                    )
        if stat_generator_key is None:
            stat_generator_keys: list[str] = self.get_all_random_generators()
            stat_generator_key = stat_generator_keys[
                random.randint(0, len(stat_generator_keys) - 1)
            ]
        # Set the stat generator if selected

        if generations_list is None:
            generations_list = Character_Generator.get_all_generators()
        generated: dict[str, Union[list[int], str]] = {}
        if "Stats" in generations_list:
            if type(stat_list) is list:
                generated["Stats"] = stat_list
            else:
                generated["Stats"] = self.generate_stat_list(stat_generator_key)
        if "Race" in generations_list:
            generated["Race"] = self.generate_race(
                Character_Generator.RACE_DICT[race_key], generator_key
            )
        if "Class" in generations_list:
            generated["Class"] = self.generate_class(
                Character_Generator.CLASS_DICT[class_key], generator_key
            )
        if "Alignment" in generations_list:
            generated["Alignment"] = self.generate_alignment(
                Character_Generator.ALIGNMENT_DICT[alignment_key], generator_key
            )
        if "Background" in generations_list:
            generated["Background"] = self.generate_background(
                Character_Generator.BACKGROUND_DICT[background_key], generator_key
            )
        return generated

    @staticmethod
    def Arrange(current_class, stat_array):
        """
        Given a class and a 6 number array it
        arranges the numbers in an optimal allocation for any given class

        Raises:
            RuntimeError: If the class does not exist
            RuntimeError: If the Array of integers is the wrong size

        Returns:
            List of stat values in the Strength Dexterity Constitution Intelligence Wisdom Charisma order
        """
        if current_class not in Character_Generator.CLASS_DICT["All"]:
            raise RuntimeError("Not a valid class")
        if len(stat_array) != 6:
            raise RuntimeError("Not a valid list")
        for i in stat_array:
            if type(i) is not int:
                raise RuntimeError("Non integer found in the list")
            if not 0 < i <= 18:
                raise RuntimeError("Invalid number")
        if len(stat_array) != 6:
            raise RuntimeError("Not a valid list")
        stat_array = sorted(stat_array)
        results = []
        if current_class == "Artificer":
            results.append(stat_array[0])
            results.append(stat_array[3])
            results.append(stat_array[4])
            results.append(stat_array[5])
            results.append(stat_array[2])
            results.append(stat_array[1])
        elif current_class == "Barbarian":
            results.append(stat_array[5])
            results.append(stat_array[3])
            results.append(stat_array[4])
            results.append(stat_array[0])
            results.append(stat_array[2])
            results.append(stat_array[1])
        elif current_class == "Bard":
            results.append(stat_array[1])
            results.append(stat_array[4])
            results.append(stat_array[3])
            results.append(stat_array[0])
            results.append(stat_array[1])
            results.append(stat_array[5])
        elif current_class == "Cleric":
            results.append(stat_array[3])
            results.append(stat_array[2])
            results.append(stat_array[4])
            results.append(stat_array[0])
            results.append(stat_array[5])
            results.append(stat_array[1])
        elif current_class == "Druid":
            results.append(stat_array[2])
            results.append(stat_array[3])
            results.append(stat_array[4])
            results.append(stat_array[1])
            results.append(stat_array[5])
            results.append(stat_array[0])
        elif current_class == "Fighter":
            results.append(stat_array[5])
            results.append(stat_array[3])
            results.append(stat_array[4])
            results.append(stat_array[0])
            results.append(stat_array[2])
            results.append(stat_array[1])
        elif current_class == "Monk":
            results.append(stat_array[2])
            results.append(stat_array[5])
            results.append(stat_array[3])
            results.append(stat_array[1])
            results.append(stat_array[4])
            results.append(stat_array[0])
        elif current_class == "Paladin":
            results.append(stat_array[5])
            results.append(stat_array[2])
            results.append(stat_array[3])
            results.append(stat_array[0])
            results.append(stat_array[1])
            results.append(stat_array[4])
        elif current_class == "Ranger":
            results.append(stat_array[2])
            results.append(stat_array[5])
            results.append(stat_array[4])
            results.append(stat_array[1])
            results.append(stat_array[3])
            results.append(stat_array[0])
        elif current_class == "Rogue":
            results.append(stat_array[0])
            results.append(stat_array[5])
            results.append(stat_array[4])
            results.append(stat_array[3])
            results.append(stat_array[1])
            results.append(stat_array[2])
        elif current_class == "Sorcerer":
            results.append(stat_array[0])
            results.append(stat_array[3])
            results.append(stat_array[4])
            results.append(stat_array[2])
            results.append(stat_array[1])
            results.append(stat_array[5])
        elif current_class == "Warlock":
            results.append(stat_array[1])
            results.append(stat_array[3])
            results.append(stat_array[4])
            results.append(stat_array[2])
            results.append(stat_array[0])
            results.append(stat_array[5])
        elif current_class == "Wizard":
            results.append(stat_array[0])
            results.append(stat_array[3])
            results.append(stat_array[4])
            results.append(stat_array[5])
            results.append(stat_array[2])
            results.append(stat_array[1])
        return results
