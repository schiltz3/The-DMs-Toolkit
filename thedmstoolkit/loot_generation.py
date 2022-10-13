import random
from toolkit.models import Armor,Weapon, GenericItem ,MagicItem, GeneratedLoot
from typing import Callable, Optional, Union

Generator = Callable[[int, int], int]


class Loot_Generator:
    total_value_to_generate = 0
    total_value_generated = 0
    continue_generating = True
    currency = 0
    loot_type = "random"
    loot_level = 1
    generator_key = "random"
    armor_list = []
    weapon_list = []
    gen_list = []
    magic_list = []
    LOOT_TYPE_DICT = {"Encounter": 1,
                      "Treasure Chest": 10,
                      "Hoard": 100,
                      "Scraps": .1,}
    
    
    Generators: dict[str, Generator] = {}
    # Unlimited Generators have a minimum range of [1,max_int]
    UnlimitedGenerators: dict[str, Generator] = {"random": random.randint}

def check_value(self):
    if self.total_value_generated > self.total_value_to_generate:
         self.continue_generating = False
             
def generate_loot_type(self):
    self.loot_type = Loot_Generator.LOOT_TYPE_LIST[Loot_Generator.Generators[self.generator_key](0, len(Loot_Generator.LOOT_TYPE_LIST)-1)]

def generate_currency(self):
     local_currency = Loot_Generator.Generators[self.generator_key](0, self.total_value_to_generate-self.total_value_generated)
     local_currency += Loot_Generator.Generators[self.generator_key](0, 100)/10
     local_currency += Loot_Generator.Generators[self.generator_key](0, 100)/100
     self.currency += local_currency
     self.total_value_generated += local_currency
     self.check_value(self)

def generate_weapon(self):
    possible_weapons = list(Weapon.objects.all())
    new_weapon = possible_weapons[Loot_Generator.Generators[self.generator_key](0, len(possible_weapons)-1)]
    self.total_value_generated += new_weapon.Base_Value
    self.weapon_list.append(new_weapon)
    self.check_value(self)

def generate_armor(self):
    possible_armor = list(Armor.objects.all())
    new_armor = possible_armor[Loot_Generator.Generators[self.generator_key](0, len(possible_armor)-1)]
    self.total_value_generated += new_armor.Base_Value
    self.armor_list.append(new_armor)
    self.check_value(self)


def generate_generic_item(self):
    possible_items = list(GenericItem.objects.all())
    new_item = possible_items[Loot_Generator.Generators[self.generator_key](0, len(possible_items)-1)]
    self.total_value_generated += new_item.Base_Value
    self.item_list.append(new_item)
    self.check_value(self)


def generate_magical_item(self):
    possible_magic_items = list(MagicItem.objects.all())
    new_magic_item = possible_magic_items[Loot_Generator.Generators[self.generator_key](0, len(possible_magic_items)-1)]
    self.continue_generating = False
    self.magic_list.append(new_magic_item)
    self.check_value(self)


def generate_total_value(self):
    self.total_value_to_generate = Loot_Generator.Generators[self.generator_key](1, 10)*self.level*Loot_Generator.LOOT_TYPE_DICT[self.loot_type]

GENERATOR_DICT = {"Currency" : generate_currency,
                      "Armor": generate_armor,
                      "Weapon": generate_weapon,
                      "Generic": generate_generic_item,
                      "Magic": generate_magical_item}
    
def generate_random(self):
    gen_keys = GENERATOR_DICT.keys
    to_generate = Loot_Generator.Generators[self.generator_key](0, len(gen_keys)-1)
    GENERATOR_DICT[gen_keys[to_generate]](self)
    
def generate_loot(self, generator_key = "random", level = 1, approximate_total_value = 0, input_loot_type = "random"):
    self.generator_key = generator_key
    if input_loot_type is "random":
        generate_loot_type(self)
    self.loot_level = level
    if approximate_total_value != 0:
        generate_total_value(self)
    else:
        self.total_value_to_generate = approximate_total_value
    
    
    while(self.continue_generating):
        generate_random(self, generator_key)
        
    current_loot = GeneratedLoot(Loot_Type = self.loot_type,
                                 Total_Value = self.total_value_to_generate,
                                 Money = self.Currency)
    for armor in self.armor_list:
        current_loot.Armors.add(armor)
    for weapon in self.weapon_list:
        current_loot.Weapons.add(weapon)
    for item in self.item_list:
        current_loot.Generic_Items.add(item)
    for magic_item in self.magic_list:
        current_loot.Magical_Items.add(magic_item)
    return current_loot
    