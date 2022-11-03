from django.contrib.auth.models import User
from django.db import models

# Create your models here.


class Character(models.Model):
    """
    Creates Characters

    Args:
        Name (String): max_length = 20, What is the character's name
        AccountOwner (ForeignKey): On delete of the owner delete all characters owned by them, Who owns this character
        Race (String): max_length = 15, What race is the character
        Class (String): max_length = 9, What class is the character
        Background (String): max_length = 22, Where did this character come from
        Alignment (String): max_length = 27, Character's Alignment
        Level (Integer): Character's Level
        Experience (Integer): Character's progress to the next level
        Strength (Integer): Monster's strength
        Dexterity (Integer): Monster's Dexterity
        Constitution (Integer): Monster's Constitution
        Intelligence (Integer): Monster's Intelligence
        Wisdom (Integer): Monster's Wisdom
        Charisma (Integer): Monster's Charisma
    Returns:
        _type_: _description_
    """

    Name = models.CharField(max_length=20)
    Owner = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    Race = models.CharField(max_length=15)
    Class = models.CharField(max_length=9)
    Background = models.CharField(max_length=22)
    Alignment = models.CharField(max_length=17)
    Level = models.IntegerField()
    Experience = models.IntegerField()
    Strength = models.IntegerField()
    Dexterity = models.IntegerField()
    Constitution = models.IntegerField()
    Intelligence = models.IntegerField()
    Wisdom = models.IntegerField()
    Charisma = models.IntegerField()

    def __str__(self):
        return self.Name + " Level " + self.Level + " " + self.Class


class Armor(models.Model):
    """
    The Model for armor used to store armor to pull from when generating loot

    Args:
        models:
        Name (String): max_length = 30, primary_key
        Description (String): max_length = 255
        Armor_Type (String): max_length = 6
        Base_Value (Double): How much it is worth based on GP
        Armor_Class_Change (Integer): How much this armor changed AC
        Weight (Integer): How much it weighs
        Stealth (Boolean): Whether or not it affects stealth True = gives disadvantage
    """

    Name = models.CharField(primary_key=True, max_length=30)
    Description = models.CharField(max_length=255)
    Armor_Type = models.CharField(max_length=6)
    Base_Value = models.FloatField()
    Armor_Class_Change = models.IntegerField()
    Weight = models.IntegerField()
    Stealth = models.BooleanField()

    def __str__(self):
        return "Armor"

class Weapon(models.Model):
    """
    The Model for weapons used to store weapons to pull from when generating loot

    Args:
        models:
        Name (String): max_length = 30, primary_key
        Damage_Type (String): max_length = 30, What kind of damage does the weapon deal
        Damage_Die (String): max_length = 14, What die to roll for damage
        Base_Value (Double): How much it is worth based on GP
        Max_Range (Integer): How far is the max range, non disadvantage range for ranged weapons is Max_Range/4
        Weight (Integer): How much it weighs
        Ammo (String): No Input is acceptable, max_length = 7, What type of ammo Arrows, Bullets, or Darts
    """

    Name = models.CharField(primary_key=True, max_length=30)
    Damage_Type = models.CharField(max_length=30)
    Weapon_Type = models.CharField(max_length=14)
    Damage_Die = models.CharField(max_length=10)
    Base_Value = models.FloatField()
    Max_Range = models.IntegerField()
    Weight = models.IntegerField()
    Ammo = models.CharField(blank=True, max_length=7)
    Special_Characteristics = models.IntegerField()
    # store as a binary where Heavy Light TwoHanded Reach Versatile Finesse Throwable Ammunition Special
    # So heavy two handed with reach would be 101100000
    
    def __str__(self):
        return "Weapon"


class GenericItem(models.Model):
    """
    The Model for generic normal items used to store items to pull from when generating loot

    Args:
        models:
        Name (String): max_length = 30, primary_key
        Description (String): max_length = 255, What is it
        Base_Value (Double): How much it is worth based on GP

    """

    Name = models.CharField(primary_key=True, max_length=30)
    Description = models.CharField(max_length=255)
    Base_Value = models.FloatField()
    
    def __str__(self):
        return "Generic"


class MagicItem(models.Model):
    """
    The Model for magical items used to store magical items to pull from when generating loot

    Args:
        models:
        Name (String): max_length = 30, primary_key
        Rarity (String): max_length = 20, What is the rarity of the item
        Effect_Description (String): max_length = 255, What does it do
        Visual_Description (String): max_length = 255, What does look like

    """

    Name = models.CharField(primary_key=True, max_length=30)
    Rarity = models.CharField(max_length=20)
    Effect_Description = models.CharField(max_length=255)
    Visual_Description = models.CharField(max_length=255)
    
    def __str__(self):
        return "Magic"


class GeneratedLoot(models.Model):
    """
    The Model for the end result of generating a loot roll

    Args:
        models:
        Loot_Type (String): max_length = 20, What kind of loot source
        Total_Value (Double): How much is it worth in total (GP)
        Money (Double): How much straight money (GP)
        Weapons (Weapon): No Input is acceptable, Which weapons are added if any
        Armors (Armor): No Input is acceptable, Which armors are added if any
        Generic_Items (GenericItem): No Input is acceptable, Which non magical items are added if any
        Magical_Items (MagicItem): No Input is acceptable, Which magic items are added if any

    """

    Owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Loot_Type = models.CharField(max_length=20)
    Total_Value = models.FloatField()
    Money = models.FloatField()
    Weapons = models.ManyToManyField(Weapon, blank=True)
    Armors = models.ManyToManyField(Armor, blank=True)
    Generic_Items = models.ManyToManyField(GenericItem, blank=True)
    Magical_Items = models.ManyToManyField(MagicItem, blank=True)


class Tag(models.Model):
    """
    Database to store the tags which will help generate monsters

    Args:
        Name (String): max_length = 30, Primary Key
    """

    Name = models.CharField(primary_key=True, max_length=30)


class Monster(models.Model):
    """
    The Model for the storing of monsters to be used as for the encounter generator

    Args:
        models:
        Name (String): max_length = 30, Primary Key Name of Monster
        Description (String): max_length = 255, What is the monster
        Challenge_Rating (Double): How strong is it
        Strength (Integer): Monster's strength
        Dexterity (Integer): Monster's Dexterity
        Constitution (Integer): Monster's Constitution
        Intelligence (Integer): Monster's Intelligence
        Wisdom (Integer): Monster's Wisdom
        Charisma (Integer): Monster's Charisma
        Gold_Modifier (Double): No Input is acceptable, How much gold is this likely to have
        Creature_Tags (Tag): No Input is acceptable, When and where should this monster be
    """

    Name = models.CharField(primary_key=True, max_length=30)
    Description = models.CharField(max_length=255)
    Challenge_Rating = models.FloatField()
    Strength = models.IntegerField()
    Dexterity = models.IntegerField()
    Constitution = models.IntegerField()
    Intelligence = models.IntegerField()
    Wisdom = models.IntegerField()
    Charisma = models.IntegerField()
    Gold_Modifier = models.FloatField(blank=True)
    Creature_Tags = models.ManyToManyField(Tag)


class GeneratedEncounter(models.Model):
    """
    The Model for the end result of generating a encounter roll

    Args:
        models:
        Encounter_Type (String): max_length = 20, What kind of encounter
        Number_Of_Characters (Integer): How many characters to generate the encounter
        Average_Character_Levels (Double): Average Character level of the characters
        Reward (GeneratedLoot): Optional, Rewards of this encounter
        Encounter_Tags(Tag): Optional, What tags are included in the generation
        Monsters (Monster): What monsters are generated

    """

    Owner = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True)
    Encounter_Type = models.CharField(max_length=20)
    Number_Of_Characters = models.IntegerField()
    Average_Character_Levels = models.FloatField()
    Reward = models.OneToOneField(
        GeneratedLoot, on_delete=models.SET_NULL, null=True, blank=True
    )
    Encounter_Tags = models.ManyToManyField(Tag, blank=True)
    Monsters = models.ManyToManyField(Monster)
