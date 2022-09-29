import random
from typing import Callable, List

from toolkit.models import Character


class Character_Generator:
    """
    Contains all the lists and Dictionaries for the various character generation methods
    """

    RaceDict: dict[str, list] = {
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
            " Kenku",
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
        "All": RaceDict["Rare"] + RaceDict["Monster"] + RaceDict["Common"],
    }
    ClassDict: dict[str, list] = {
        "Martial": ["Fighter", "Monk", "Ranger", "Rogue"],
        "Divine": ["Cleric", "Paladin", "Warlock"],
        "Magic": ["Artificer", "Bard", "Druid", "Sorcerer", "Wizard"],
        "All": ClassDict["Martial"] + ClassDict["Divine"] + ClassDict["Magic"],
    }
    AlignmentDict: dict[str, list] = {
        "Good": ["Lawful Good", "Neutral Good", "Chaotic Good"],
        "Neutral": ["Lawful Neutral", "True Neutral", "Chaotic Neutral"],
        "Evil": ["Lawful Evil", "Neutral Evil", "Chaotic Evil"],
        "All": AlignmentDict["Good"] + AlignmentDict["Neutral"] + AlignmentDict["Evil"],
    }
    MethodDict: dict[str, list] = {
        "StandardArray": [15, 14, 13, 12, 10, 8],
        "3d6": [
            random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6),
            random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6),
            random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6),
            random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6),
            random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6),
            random.randint(1, 6) + random.randint(1, 6) + random.randint(1, 6),
        ],
    }
    BackgroundList = [
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

    

    def get_Generators(self,Key):
        """
        Gives the list of generator keys
        Returns:
            List: a list of all generator keys
        """
        return Character_Generator.GeneratorList.keys

    def Generate_Stats(self,StatList):
        """Returns the Stat List needed because the dictionary is in str:function

        Args:
            StatList (List): List of stat values

        Returns:
            StatList (List): List of stat values
        """
        return StatList

    def Generate_Race(self,RaceList) -> str:
        """
        Generates a race from the provided list
        Args:
            RaceList (list): The list chosen from thr dictionary
        Returns:
            String: Race
        """
        Race = RaceList[random.randint[0, RaceList.len - 1]]
        return Race

    def Generate_Class(self,ClassList) -> str:
        """
        Returns a random class from the provided list
        Args:
            ClassList (List): The list chosen from the Class dictionary

        Returns:
            String: the random class
        """
        Class = ClassList[random.randint[0, ClassList.len - 1]]
        return Class

    def Generate_Alignment(self, AlignmentList) -> str:
        """
            Returns a random alignment from the provided list
        Args:
            AlignmentList (List): List of alignments from alignment dictionary

        Returns:
            String: Alignment
        """
        Alignment = AlignmentList[random.randint[0, AlignmentList.len - 1]]
        return Alignment

    def Generate_Background(self, BackgroundList) -> str:
        """
            Generate a random
        Args:
            BackgroundList (_type_): _description_
        """
        return BackgroundList[random.randint[0, BackgroundList.len - 1]]
    def Generate(self, Generator):
        """
        Given the generator key it runs that generator
        Args:
            Generator (String): The key to the generator dictionary

        Returns:
            Returns the thing you want generated
        """
        GeneratorList: dict[str, any] = {
        "Stats": Generate_Stats(MethodDict[Key]),
        "Race": Generate_Race(RaceDict[Key]),
        "Class": Generate_Class(ClassDict[Key]),
        "Alignment": Generate_Alignment(AlignmentDict[Key]),
        "Background": Generate_Background(BackgroundList[Key]),
    }
        return GeneratorList[Generator]

    def Arrange(self, CharacterID, StatArray):
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
