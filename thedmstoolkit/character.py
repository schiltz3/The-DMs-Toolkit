from toolkit.models import Character
import random
def GenerateStats(CharacterID, Key):
    """Provided a character ID and the key to the method of generating stats it generates an array
    and passes it to arrange in-order to save it to that character in the right place

    Args:
        CharacterID (int): Primary Key to the Character being generated
        Key (String): Key to the dictionary of methods to generate stats
    """    
    MethodDictionary = dict["StandardArray":[15,14,13,12,10,8],
                            "3d6":[random.randint(1,6)+random.randint(1,6)+random.randint(1,6),
                                   random.randint(1,6)+random.randint(1,6)+random.randint(1,6),
                                   random.randint(1,6)+random.randint(1,6)+random.randint(1,6),
                                   random.randint(1,6)+random.randint(1,6)+random.randint(1,6),
                                   random.randint(1,6)+random.randint(1,6)+random.randint(1,6),
                                   random.randint(1,6)+random.randint(1,6)+random.randint(1,6)]]
    Arrange(CharacterID, MethodDictionary[Key])
    
def GenerateRace(CharacterID):
    pass

def GenerateClass(CharacterID):
    pass

def GenerateAlignment(CharacterID):
    pass

def GenerateBackground(CharacterID):
    pass

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
