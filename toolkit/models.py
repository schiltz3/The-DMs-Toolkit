from django.contrib.auth.models import User
from django.db import models
from django.db.models.signals import post_save
from django.dispatch import receiver

# Create your models here.

class Proficiencies(models.Model):
    """
    Proficiencies

    Args:
        Name-String
        Stat- relevant stat

    Returns:
        Proficiency object
    """

    Name = models.CharField(max_length=20, blank=True)
    Stat = models.CharField(max_length=20, blank=True)
    def __str__(self):
        return self.Name
    

class Race(models.Model):
    """_summary_

    Args:
        Name = String
        Speed = Integer

    Returns:
        Race object
    """
    Name = models.CharField(max_length=20)
    Speed = models.IntegerField()
    Monster = "Monster"
    Rare = "Rare"
    Common = "Common"
    Options = [(Monster, "Monster"),(Rare, "Rare"), (Common, "Common")]
    def __str__(self):
        return self.Name
    
class Clazz(models.Model):
    """Creates Class

    Args:
        Name = String
        Proficiencies = Many to Many
    """    
    Name = models.CharField
    Magic = "Magic"
    Martial = "Martial"
    Divine = "Divine"
    Options = [(Magic, "Magic"), (Martial, "Martial"), (Divine, "Divine")] 
    Proficiencies = models.ManyToManyField(Proficiencies)
    StatPrecedence = models.CharField(max_length=20)
    def __str__(self):
        return self.Name

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
    Race = models.ForeignKey(Race,on_delete=models.SET_NULL, null = True, blank=True,default=None)
    Class = models.ForeignKey(Clazz, on_delete=models.SET_NULL,null = True,blank=True, default=None)
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
    Character_Proficiencies = models.ManyToManyField(
        Proficiencies, blank=True, default=""
    )

    def __str__(self):
        return f"Name: {self.Name}, Owner: {self.Owner}, lvl: {self.Level}, Class: {self.Class}"


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
    Armor_Type = models.CharField(max_length=6)
    Base_Value = models.FloatField()
    Armor_Class_Change = models.CharField(max_length=50)
    Weight = models.IntegerField()
    Stealth = models.BooleanField()

    def __str__(self):
        return self.Name

    @property
    def type(self):
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
    Special_Characteristics = models.IntegerField(blank=True, null=True)
    # store as a binary where Heavy Light TwoHanded Reach Versatile Finesse Throwable Ammunition Special
    # So heavy two handed with reach would be 101100000

    def __str__(self):
        return self.Name

    @property
    def type(self):
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
    Weight = models.IntegerField(blank=True, null=True)

    def __str__(self):
        return self.Name

    @property
    def type(self):
        return "Generic Item"


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
    Type = models.CharField(max_length=30)
    Attuned = models.BooleanField()

    def __str__(self):
        return self.Name

    @property
    def type(self):
        return "Magic Item"


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

    def __str__(self) -> str:
        return f"{self.Owner},\t{self.Loot_Type},\tTotal Value: {self.Total_Value}"


class Tag(models.Model):
    """
    Database to store the tags which will help generate monsters

    Args:
        Name (String): max_length = 30, Primary Key
    """

    Name = models.CharField(primary_key=True, max_length=30)

    def __str__(self) -> str:
        return f"{self.Name}"


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
    Challenge_Rating = models.FloatField()
    Size = models.CharField(max_length=20)
    Type = models.CharField(max_length=20)
    Alignment = models.CharField(max_length=20)
    Armor_Class = models.IntegerField(blank=True, null=True)
    Hitpoints = models.IntegerField(blank=True, null=True)
    Initiative = models.IntegerField(blank=True, null=True)
    Gold_Modifier = models.FloatField(blank=True, null=True)
    Creature_Tags = models.ManyToManyField(Tag, blank=True)
    Source = models.CharField(max_length=30)

    def __str__(self) -> str:
        return self.Name


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
    Average_CR = models.FloatField(default=0)
    Encounter_Tags = models.ManyToManyField(Tag, blank=True)
    Monsters = models.ManyToManyField(Monster)

    def __str__(self) -> str:
        return f"{self.Owner},\t{self.Encounter_Type},\t{self.Monsters}"

class Source(models.Model):
    """Source database

    Args:
        Type, name, shortname link =  strings
    """    
    Type = models.CharField(max_length=20)
    Name = models.CharField(max_length=20)
    ShortName = models.CharField(max_length=20)
    Link = models.CharField(max_length=200)
    def __str__(self):
        return self.Name

class Cache(models.Model):
    """
    The model to cache generated items in before saving

    Args:
        user (User): user to cache generated items for
        character (Character): character to cache
    """

    user = models.OneToOneField(User, on_delete=models.CASCADE)
    character = models.OneToOneField(
        Character, on_delete=models.CASCADE, null=True, blank=True
    )
    loot = models.OneToOneField(
        GeneratedLoot, on_delete=models.CASCADE, null=True, blank=True
    )
    encounter = models.OneToOneField(
        GeneratedEncounter, on_delete=models.CASCADE, null=True, blank=True
    )

    def __str__(self) -> str:
        return f"{self.user},\t{self.character},\t{self.loot},\t{self.encounter}"


@receiver(post_save, sender=User)
def create_user_cache(sender, instance, created, **kwargs):
    """Create a cache object when creating the user object"""
    if created:
        Cache.objects.create(user=instance)


@receiver(post_save, sender=User)
def save_user_cache(sender, instance, **kwargs):
    """Save the cache object when saving the user object"""
    instance.cache.save()
