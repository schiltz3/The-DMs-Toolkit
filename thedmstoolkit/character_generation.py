import random
from typing import Callable, Optional

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
    STANDARD_ARRAY: list[int] = [15, 14, 13, 12, 10, 8]

    @staticmethod
    def three_d_six(low, high) -> int:
        return random.randint(1, 6)

    # Unlimited Generators have a minimum range of [1,max_int]
    UnlimitedGenerators: dict[str, Generator] = {"random": random.randint}
    # Limited Generators have a max range of [1,20], and therefore are not suitable for use in generating race, class, etc
    LimitedGenerators: dict[str, Generator] = {
        "3d6": three_d_six,
    }

    def __init__(
        self,
    ):
        self.Generators: dict[str, Generator] = {
            **self.LimitedGenerators,
            **self.UnlimitedGenerators,
        }
        # TODO: Put list concatenation here

    def get_all_generators(self):
        """
        Gives the list of generator keys
        Returns:
            List: a list of all generator keys
        #TODO: could just replace generator list here
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

    @staticmethod
    def generate_stat_list(generator: Generator):
        """Returns the Stat List needed because the dictionary is in str:function

        Args:
            generator (Callable): random number generator

        Returns:
            StatList (List): List of stat values
        """

        stat_list = [generator(1, 20) for _ in range(5)]
        return stat_list

    @staticmethod
    def generate_race(race_list: list[str], generator: Generator) -> str:
        """
        Generates a race from the provided list
        Args:
            RaceList (list): The list chosen from thr dictionary
            generator (Callable): random number generator
        Returns:
            String: Race
        """
        Race: str = race_list[generator(0, len(race_list))]
        return Race

    @staticmethod
    def generate_class(class_list: list[str], generator: Generator) -> str:
        """
        Returns a random class from the provided list
        Args:
            class_list (List): The list chosen from the Class dictionary
            generator (Callable): random number generator

        Returns:
            String: the random class
        """
        clazz: str = class_list[generator(0, len(class_list))]
        return clazz

    @staticmethod
    def generate_alignment(alignment_list: list[str], generator: Generator) -> str:
        """
            Returns a random alignment from the provided list
        Args:
            AlignmentList (List): List of alignments from alignment dictionary
            generator (Callable): random number generator

        Returns:
            String: Alignment
        """
        alignment = alignment_list[generator(0, len(alignment_list))]
        return alignment

    @staticmethod
    def generate_background(background_list: list[str], generator: Generator) -> str:
        """
            Generate a random background
        Args:
            background_list (str): background
            generator (Callable): random number generator
        """
        return background_list[generator(0, len(background_list))]

    def Generate(
        self,
        generator_key="All",
        stat_generator_key: Optional[str] = None,
        race_key="All",
        class_key="All",
        alignment_key="All",
        background_key="All",
        stat_list=Optional[list[int]],
    ) -> dict[str, list[int] | str]:
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
        # TODO: put in input validation

        if stat_list & len(stat_list) != 6:
            raise ValueError("Stat list length must be 6")
        if generator_key == "All":
            generator_keys: list[str] = self.get_all_generators()
            generator_key = generator_keys[random.randint(0, len(generator_keys) - 1)]
        if stat_generator_key == "All":
            stat_generator_keys: list[str] = self.get_limited_generators()
            stat_generator_key = stat_generator_keys[
                random.randint(0, len(generator_keys) - 1)
            ]
        generator = self.Generators[generator_key]
        # Set the stat generator if selected
        stat_generator = (
            generator
            if not stat_generator_key
            else self.LimitedGenerators[stat_generator_key]
        )

        generated_list: dict[str, list[int] | str] = {
            "Stats": stat_list
            if stat_list
            else self.generate_stat_list(stat_generator),
            "Race": self.generate_race(self.RACE_DICT[race_key], generator),
            "Class": self.generate_class(self.CLASS_DICT[class_key], generator),
            "Alignment": self.generate_alignment(
                self.ALIGNMENT_DICT[alignment_key], generator
            ),
            "Background": self.generate_background(
                self.BACKGROUND_LIST[background_key], generator
            ),
        }
        return generated_list

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
