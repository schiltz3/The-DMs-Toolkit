import random
from typing import Callable, Optional, Union

from toolkit.models import Character

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
    BACKGROUND_LIST = [
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
    GENERATOR_LIST: list[str] = ["Stats", "Race", "Class", "Alignment", "Background"]
    STANDARD_ARRAY: list[int] = [15, 14, 13, 12, 10, 8]

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

    Generators: dict[str, Generator] = {}
    # Unlimited Generators have a minimum range of [1,max_int]
    UnlimitedGenerators: dict[str, Generator] = {"random": random.randint}
    # Limited Generators have a max range of [1,20], and therefore are not suitable for use in generating race, class, etc
    LimitedGenerators: dict[str, Generator] = {
        "3d6": three_d_six,
    }
    Generators.update(LimitedGenerators)
    Generators.update(UnlimitedGenerators)

    def __init__(self):
        pass
        # self.Generators: dict[str, Generator] = {
        #    **self.LimitedGenerators,
        #    **self.UnlimitedGenerators,

    #  }

    def get_all_generators(self):
        """
        Gives the list of generator keys
        Returns:
            List: a list of all generator keys
        """
        return self.GENERATOR_LIST

    def get_all_random_generators(self):
        """
        Gives the list of random generator keys
        Returns:
            List: a list of all generator keys
        """
        return self.Generators.keys()

    def get_limited_generators(self):
        """
        Gives the list of limited generator keys
        Returns:
            List: a list of all limited generator keys
        """
        return self.LimitedGenerators.keys()

    def get_unlimited_generators(self):
        """
        Gives the list of unlimited generator keys
        Returns:
            List: a list of all unlimited generator keys
        """
        return self.UnlimitedGenerators.keys()

    def generate_stat_list(self, GeneratorKey: str):
        """Returns the Stat List needed because the dictionary is in str:function

        Args:
            generator (Callable): random number generator

        Returns:
            StatList (List): List of stat values
        """
        if GeneratorKey not in list(self.Generators.keys()):
            raise RuntimeError("Generator does not exist")
        stat_list = [self.Generators[GeneratorKey](1, 20) for _ in range(5)]
        return stat_list

    def generate_race(self, race_list: list[str], GeneratorKey: str) -> str:
        """
        Generates a race from the provided list
        Args:
            RaceList (list): The list chosen from thr dictionary
            generator (Callable): random number generator
        Returns:
            String: Race
        """
        if GeneratorKey not in list(self.Generators.keys()):
            raise RuntimeError("Generator does not exist")
        if race_list not in self.RACE_DICT.items():
            raise RuntimeError("Invalid List")
        Race: str = race_list[self.Generators[GeneratorKey](0, len(race_list) - 1)]
        return Race

    def generate_class(self, class_list: list[str], GeneratorKey: str) -> str:
        """
        Returns a random class from the provided list
        Args:
            class_list (List): The list chosen from the Class dictionary
            generator (Callable): random number generator

        Returns:
            String: the random class
        """
        if GeneratorKey not in list(self.Generators.keys()):
            raise RuntimeError("Generator does not exist")
        if class_list not in self.CLASS_DICT.items():
            raise RuntimeError("Invalid List")
        clazz: str = class_list[self.Generators[GeneratorKey](0, len(class_list) - 1)]
        return clazz

    def generate_alignment(self, alignment_list: list[str], GeneratorKey: str) -> str:
        """
            Returns a random alignment from the provided list
        Args:
            AlignmentList (List): List of alignments from alignment dictionary
            generator (Callable): random number generator

        Returns:
            String: Alignment
        """
        if GeneratorKey not in list(self.Generators.keys()):
            raise RuntimeError("Generator does not exist")
        if alignment_list not in self.ALIGNMENT_DICT.items():
            raise RuntimeError("Invalid List")
        alignment = alignment_list[
            self.Generators[GeneratorKey](0, len(alignment_list) - 1)
        ]
        return alignment

    def generate_background(self, background_list: list[str], GeneratorKey: str) -> str:
        """
            Generate a random background
        Args:
            background_list (str): background
            generator (Callable): random number generator
        """
        if GeneratorKey not in list(self.Generators.keys()):
            raise RuntimeError("Generator does not exist")
        if background_list != self.BACKGROUND_LIST:
            raise RuntimeError("Invalid List")
        return background_list[
            self.Generators[GeneratorKey](0, len(background_list) - 1)
        ]

    def Generate(
        self,
        GenerationsList="All",
        stat_generator_key: Optional[str] = None,
        race_key="All",
        class_key="All",
        alignment_key="All",
        GeneratorKey="random",
        stat_list=Optional[list[int]],
    ) -> dict[str, Union[list[int], str]]:
        """Given generator parameters, return a dictionary of character characteristics

        Args:
            generator_key (str, optional): A generator name from unlimited_generators(). Defaults to "All".
            stat_generator_key (Optional[str], optional): A generator name from limited_generators(). Defaults to None.
            race_key (str, optional): A race name, from the RACE_DICT. Defaults to "All".
            class_key (str, optional): A class name from the CLASS_DICT. Defaults to "All".
            alignment_key (str, optional): A alignment name from the ALIGNMENT_DICT. Defaults to "All".
            background_key (str, optional): A background name from the BACKGROUND_DICT. Defaults to "All".
            stat_list (list[int], optional): A list of 6 numbers between 1 and 20 to use as stats. Defaults to None.

        Raises:
            ValueError: _description_

        Returns:
            dict[str, list[int] | str]: Generated Characteristics
        """

        if stat_list & len(stat_list) != 6:
            raise ValueError("Stat list length must be 6")
        if stat_list:
            for i in stat_list:
                if type(i) != int:
                    raise RuntimeError("Not all numbers in Stat array are integers")
                if not 0 < i <= 18:
                    raise RuntimeError(
                        "There is an invalid number in the array, please use 1-18"
                    )
        if stat_generator_key is None:
            stat_generator_keys: list[str] = self.get_limited_generators()
            stat_generator_key = stat_generator_keys[
                random.randint(0, len(stat_generator_keys) - 1)
            ]
        # Set the stat generator if selected

        if GenerationsList == "All":
            GenerationsList = self.get_all_generators()
        generated: dict[str, Union[list[int], str]] = {}
        if "Stats" in GenerationsList:
            if stat_list:
                generated.update({"Stats": stat_list})
            else:
                generated.update({"Stats": self.generate_stat_list(stat_generator_key)})
        if "Race" in GenerationsList:
            generated.update(
                {"Race": self.generate_race(self.RACE_DICT[race_key], GeneratorKey)}
            )
        if "Class" in GenerationsList:
            generated.update(
                {"Class": self.generate_class(self.CLASS_DICT[class_key], GeneratorKey)}
            )
        if "Alignment" in GenerationsList:
            generated.update(
                {
                    "Alignment": self.generate_alignment(
                        self.ALIGNMENT_DICT[alignment_key], GeneratorKey
                    )
                }
            )
        if "Background" in GenerationsList:
            generated.update(
                {
                    "Background": self.generate_background(
                        self.BACKGROUND_LIST, GeneratorKey
                    )
                }
            )
        return generated

    @staticmethod
    def Arrange(CharacterID, StatArray):
        """
        Given a character ID and a 6 number array it
        arranges the numbers in an optimal allocation for any given class

        Raises:
            RuntimeError: If the character is does not exist
            RuntimeError: If the Array of integers is the wrong size
        """
        check = Character.objects.filter(id=CharacterID)
        if check.count == 0:
            raise RuntimeError("Character does not exist")
        CurrentCharacter = Character.objects.get(id=CharacterID)
        CurrentClass = CurrentCharacter.Class
        StatArray = sorted(StatArray)
        if CurrentClass == "Artificer":
            CurrentCharacter.Strength = StatArray[0]
            CurrentCharacter.Dexterity = StatArray[3]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[5]
            CurrentCharacter.Wisdom = StatArray[2]
            CurrentCharacter.Charisma = StatArray[1]
        elif CurrentClass == "Barbarian":
            CurrentCharacter.Strength = StatArray[5]
            CurrentCharacter.Dexterity = StatArray[3]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[0]
            CurrentCharacter.Wisdom = StatArray[2]
            CurrentCharacter.Charisma = StatArray[1]
        elif CurrentClass == "Bard":
            CurrentCharacter.Strength = StatArray[1]
            CurrentCharacter.Dexterity = StatArray[4]
            CurrentCharacter.Constitution = StatArray[3]
            CurrentCharacter.Intelligence = StatArray[0]
            CurrentCharacter.Wisdom = StatArray[1]
            CurrentCharacter.Charisma = StatArray[5]
        elif CurrentClass == "Cleric":
            CurrentCharacter.Strength = StatArray[3]
            CurrentCharacter.Dexterity = StatArray[2]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[0]
            CurrentCharacter.Wisdom = StatArray[5]
            CurrentCharacter.Charisma = StatArray[1]
        elif CurrentClass == "Druid":
            CurrentCharacter.Strength = StatArray[2]
            CurrentCharacter.Dexterity = StatArray[3]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[1]
            CurrentCharacter.Wisdom = StatArray[5]
            CurrentCharacter.Charisma = StatArray[0]
        elif CurrentClass == "Fighter":
            CurrentCharacter.Strength = StatArray[5]
            CurrentCharacter.Dexterity = StatArray[3]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[0]
            CurrentCharacter.Wisdom = StatArray[2]
            CurrentCharacter.Charisma = StatArray[1]
        elif CurrentClass == "Monk":
            CurrentCharacter.Strength = StatArray[2]
            CurrentCharacter.Dexterity = StatArray[5]
            CurrentCharacter.Constitution = StatArray[3]
            CurrentCharacter.Intelligence = StatArray[1]
            CurrentCharacter.Wisdom = StatArray[4]
            CurrentCharacter.Charisma = StatArray[0]
        elif CurrentClass == "Paladin":
            CurrentCharacter.Strength = StatArray[5]
            CurrentCharacter.Dexterity = StatArray[2]
            CurrentCharacter.Constitution = StatArray[3]
            CurrentCharacter.Intelligence = StatArray[0]
            CurrentCharacter.Wisdom = StatArray[1]
            CurrentCharacter.Charisma = StatArray[4]
        elif CurrentClass == "Ranger":
            CurrentCharacter.Strength = StatArray[2]
            CurrentCharacter.Dexterity = StatArray[5]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[1]
            CurrentCharacter.Wisdom = StatArray[3]
            CurrentCharacter.Charisma = StatArray[0]
        elif CurrentClass == "Rogue":
            CurrentCharacter.Strength = StatArray[0]
            CurrentCharacter.Dexterity = StatArray[5]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[3]
            CurrentCharacter.Wisdom = StatArray[1]
            CurrentCharacter.Charisma = StatArray[2]
        elif CurrentClass == "Sorcerer":
            CurrentCharacter.Strength = StatArray[0]
            CurrentCharacter.Dexterity = StatArray[3]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[2]
            CurrentCharacter.Wisdom = StatArray[1]
            CurrentCharacter.Charisma = StatArray[5]
        elif CurrentClass == "Warlock":
            CurrentCharacter.Strength = StatArray[1]
            CurrentCharacter.Dexterity = StatArray[3]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[2]
            CurrentCharacter.Wisdom = StatArray[0]
            CurrentCharacter.Charisma = StatArray[5]
        elif CurrentClass == "Wizard":
            CurrentCharacter.Strength = StatArray[0]
            CurrentCharacter.Dexterity = StatArray[3]
            CurrentCharacter.Constitution = StatArray[4]
            CurrentCharacter.Intelligence = StatArray[5]
            CurrentCharacter.Wisdom = StatArray[2]
            CurrentCharacter.Charisma = StatArray[1]
        CurrentCharacter.save()
