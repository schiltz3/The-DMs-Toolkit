import django
from django.test import TestCase

import toolkit.views.loot_generator.loot_generation as Loot_Gen
from toolkit.models import Armor, GenericItem, MagicItem, Weapon

django.setup()


class PositiveTests(TestCase):
    """
    Loot Tests that should succeed

    Args:
        TestCase (_type_): Django Tests
    """
    
    def setUp(self):
        """Set up a generator for each test"""
        self.gen_key = "Random"

    def test_check_value(self):
        """Tests for the check value function"""
        new_loot = Loot_Gen.Loot_Generator()
        new_loot.min_value_to_generate = 1000
        new_loot.check_value()
        self.assertTrue(new_loot.continue_generating)

        new_loot.total_value_generated = 1001
        new_loot.check_value()
        self.assertFalse(new_loot.continue_generating)

    def test_generate_loot_type(self):
        """Tests for the generate loot type"""
        new_loot = Loot_Gen.Loot_Generator()
        new_loot.generate_loot_type()
        self.assertTrue(new_loot.loot_type in list(new_loot.LOOT_TYPE_DICT.keys()))

    def test_currency(self):
        """Tests for generate currency"""
        new_loot = Loot_Gen.Loot_Generator()
        new_loot.min_value_to_generate = 1000
        new_loot.generate_currency()
        self.assertTrue(new_loot.currency > 0)

    def test_armor(self):
        """tests for generate armor"""
        armor = Armor(
            Name="Plate",
            Description="Plate Armor",
            Armor_Type="Heavy",
            Base_Value=2.1,
            Armor_Class_Change=2,
            Weight=50,
            Stealth=True,
        )
        armor.save()

        new_loot = Loot_Gen.Loot_Generator()
        new_loot.generate_armor()
        self.assertTrue(armor in new_loot.armor_list)

    def test_weapons(self):
        """tests for generate weapons"""
        weapon = Weapon(
            Name="Axe",
            Damage_Type="Slashing",
            Damage_Die="1d12",
            Base_Value=1.2,
            Max_Range=5,
            Weight=10,
            Special_Characteristics=101000000,
        )
        weapon.save()

        new_loot = Loot_Gen.Loot_Generator()
        new_loot.generate_weapon()
        self.assertTrue(weapon in new_loot.weapon_list)

    def test_generic(self):
        """tests for generate generic items"""
        item = GenericItem(Name="Rope", Description="It's Rope", Base_Value=0.01)
        item.save()

        new_loot = Loot_Gen.Loot_Generator()
        new_loot.generate_generic_item()
        self.assertTrue(item in new_loot.gen_list)

    def test_magic(self):
        """tests for generate magic items"""
        mitem = MagicItem(
            Name="Rope",
            Rarity="Common",
            Effect_Description="It does something special",
            Visual_Description="It's rope but magic",
        )
        mitem.save()

        new_loot = Loot_Gen.Loot_Generator()
        new_loot.generate_magical_item()
        self.assertTrue(mitem in new_loot.magic_list)
        self.assertFalse(new_loot.continue_generating)

    def test_total_value(self):
        """tests for generate a random total value"""
        new_loot = Loot_Gen.Loot_Generator()
        new_loot.loot_type = "Encounter"

        new_loot.generate_total_value()
        self.assertTrue(new_loot.min_value_to_generate > 0)

    def test_random(self):
        """tests for generate random item of any type"""
        mitem = MagicItem(
            Name="Rope",
            Rarity="Common",
            Effect_Description="It does something special",
            Visual_Description="It's rope but magic",
        )
        mitem.save()

        item = GenericItem(Name="Rope", Description="It's Rope", Base_Value=0.01)
        item.save()

        weapon = Weapon(
            Name="Axe",
            Damage_Type="Slashing",
            Damage_Die="1d12",
            Base_Value=1.2,
            Max_Range=5,
            Weight=10,
            Special_Characteristics=101000000,
        )
        weapon.save()

        armor = Armor(
            Name="Plate",
            Description="Plate Armor",
            Armor_Type="Heavy",
            Base_Value=2.1,
            Armor_Class_Change=2,
            Weight=50,
            Stealth=True,
        )
        armor.save()

        new_loot = Loot_Gen.Loot_Generator()
        new_loot.generate_random()
        self.assertTrue(new_loot.total_value_generated > 0)

    def test_generate(self):
        """Tests for the overall generate loot function"""
        mitem = MagicItem(
            Name="Rope",
            Rarity="Common",
            Effect_Description="It does something special",
            Visual_Description="It's rope but magic",
        )
        mitem.save()

        item = GenericItem(Name="Rope", Description="It's Rope", Base_Value=0.01)
        item.save()

        weapon = Weapon(
            Name="Axe",
            Damage_Type="Slashing",
            Damage_Die="1d12",
            Base_Value=1.2,
            Max_Range=5,
            Weight=10,
            Special_Characteristics=101000000,
        )
        weapon.save()

        armor = Armor(
            Name="Plate",
            Description="Plate Armor",
            Armor_Type="Heavy",
            Base_Value=2.1,
            Armor_Class_Change=2,
            Weight=50,
            Stealth=True,
        )
        armor.save()

        new_loot = Loot_Gen.Loot_Generator()
        result = new_loot.generate_loot()
        self.assertTrue(result["loot_object"].Total_Value > 0)
        result2 = new_loot.generate_loot(generator_key=self.gen_key)
        self.assertTrue(result2["loot_object"].Total_Value > 0)
        result3 = new_loot.generate_loot(generator_key=self.gen_key, level=10)
        self.assertTrue(result3["loot_object"].Total_Value > 0)
        result4 = new_loot.generate_loot(
            generator_key=self.gen_key, level=10, approximate_total_value=22
        )
        self.assertTrue(result4["loot_object"].Total_Value > 0)
        result5 = new_loot.generate_loot(
            generator_key=self.gen_key, level=10, input_loot_type="Hoard"
        )
        self.assertTrue(result5["loot_object"].Total_Value > 0)


class negative_tests(TestCase):
    """
    Tests that should raise exceptions
    Args:
        TestCase (_type_): Django tests
    """
    
    def setUp(self):
        """Set up a generator for each test"""
        self.gen_key = "Random"

    def test_generate(self):
        """Tests on the various inputs of the generate loot function"""
        new_loot = Loot_Gen.Loot_Generator()
        with self.assertRaises(
            ValueError, msg="Shouldn't accept that as a generator key"
        ):
            new_loot.generate_loot("bacon")
        with self.assertRaises(ValueError, msg="Shouldn't accept that as a option"):
            new_loot.generate_loot(self.gen_key, "lettuce")
        with self.assertRaises(ValueError, msg="Shouldn't accept that as a option"):
            new_loot.generate_loot(self.gen_key, 30)
        with self.assertRaises(ValueError, msg="Shouldn't accept that as a option"):
            new_loot.generate_loot(self.gen_key, 11, "tomato")
        with self.assertRaises(ValueError, msg="Shouldn't accept that as a option"):
            new_loot.generate_loot(self.gen_key, 11, -1)
        with self.assertRaises(ValueError, msg="Shouldn't accept that as a option"):
            new_loot.generate_loot(self.gen_key, 11, 100, "Nothing")
        with self.assertRaises(Exception, msg="Shouldn't accept that as a option"):
            new_loot.generate_loot(self.gen_key, 11, 100, "Horde", "TooMuch")
