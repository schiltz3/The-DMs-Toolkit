import django
from django.test import TestCase

import toolkit.views.encounter_generator.encounter_generation as enc_gen
from toolkit.models import Armor, GenericItem, MagicItem, Monster, Tag, Weapon

django.setup()


class Tag_Tests(TestCase):
    """Tests for Tag methods

    Args:
        TestCase (_type_): Django Test Module
    """

    def setUp(self):
        """Setting up for tests"""
        self.encounter = enc_gen.Encounter_Generator()
        self.new_tag = Tag(Name="Test")

        self.tag1 = Tag(Name="Test1")
        self.tag2 = Tag(Name="Test2")
        self.tag2.save()
        self.tag1 = Tag(Name="Test3")
        self.tag1.save()
        self.tag2 = Tag(Name="Test 4")
        self.tag2.save()
        self.tag_error = Tag(Name="Error")
        self.encounter.tags.append(self.new_tag)
        self.encounter.tags.append(self.tag1)
        self.encounter.tags.append(self.tag2)

    def test_get_tags_negative(self):
        """Tests for getting tag negative"""
        self.assertNotIn(
            self.tag_error, self.encounter.get_tags(), msg="Tag should not be present"
        )

    def test_get_tags_positive(self):
        """Tests for getting tag"""
        self.encounter.tags.append(self.new_tag)
        self.assertIn(
            self.new_tag, self.encounter.get_tags(), msg="Tag not in the list"
        )

    def test_add_tags_negative(self):
        """Tests for adding tags"""
        with self.assertRaises(
            ValueError, msg="Should not accept a nonexistant tag name"
        ):
            self.encounter.add_tag("Error")
        with self.assertRaises(
            ValueError, msg="Should not accept a nonstring tag name"
        ):
            self.encounter.add_tag(1)
        with self.assertRaises(
            ValueError, msg="Should not accept a tag not in the database"
        ):
            self.encounter.add_tag(self.tag_error)

    def test_add_tags_positive(self):
        """Tests for adding tags"""
        self.tag1.save()
        self.encounter.add_tag(self.tag1)
        self.assertIn(self.tag1, self.encounter.tags)
        self.encounter.add_tag("Test2")
        self.assertIn(self.tag2, self.encounter.tags)

    def test_remove_tags_negative(self):
        """Tests for removing tags"""
        with self.assertRaises(ValueError):
            self.encounter.remove_tag("Error")
        with self.assertRaises(ValueError):
            self.encounter.remove_tag(self.tag_error)
        with self.assertRaises(ValueError):
            self.encounter.remove_tag(1)

    def test_remove_tags_positive(self):
        """Tests for removing tags"""
        self.encounter.remove_tag(self.tag1)
        self.assertNotIn(self.tag1, self.encounter.tags)
        self.encounter.remove_tag("Test 4")
        self.assertNotIn(self.tag2, self.encounter.tags)


class Level_Tests(TestCase):
    """Tests for Level methods

    Args:
        TestCase (_type_): Django Test Module
    """

    def setUp(self):
        """Tests Setup"""
        self.encounter = enc_gen.Encounter_Generator()

    def test_get_level(self):
        """Tests for get level"""
        self.assertEqual(1, self.encounter.average_party_level)

    def test_set_level_positive(self):
        """Tests for set level"""
        self.encounter.change_average_level(11)
        self.assertEqual(11, self.encounter.average_party_level)
        self.encounter.change_average_level(13.5)
        self.assertEqual(13.5, self.encounter.average_party_level)

    def test_set_level_negative(self):
        """Tests for set level"""
        with self.assertRaises(ValueError):
            self.encounter.change_average_level("Error")
        with self.assertRaises(ValueError):
            self.encounter.change_average_level(40)


class Encounter_Type_Tests(TestCase):
    """Tests for Encounter Type methods

    Args:
        TestCase (_type_): Django Test Module
    """

    def setUp(self):
        """Tests setup"""
        self.encounter = enc_gen.Encounter_Generator()

    def test_get_encounter_type(self):
        """Tests get encounter types"""
        self.assertEqual(self.encounter.get_encounter_type(), "Average Encounter")

    def test_set_encounter_type_positive(self):
        """Tests set encounter types"""
        self.encounter.set_encounter_type("Horde")
        self.assertEqual(self.encounter.encounter_type, "Horde")

    def test_set_encounter_type_negative(self):
        """Tests set encounter types"""
        with self.assertRaises(ValueError):
            self.encounter.set_encounter_type(1)


class Loot_Tests(TestCase):
    """Tests for loot methods

    Args:
        TestCase (_type_): Django Test Module
    """

    def setUp(self):
        """Test setup"""
        self.encounter = enc_gen.Encounter_Generator()
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

    def test_generate_loot(self):
        """Tests for generating loot"""
        self.encounter.generate_loot()
        self.assertNotEqual(self.encounter.dropped_loot, None)

    def test_get_loot(self):
        """Tests for returning loot"""
        loot = self.encounter.dropped_loot
        self.assertEqual(self.encounter.get_loot(), loot)

    def test_get_loot_modifier(self):
        """Tests for getting loot modifier"""
        mod = self.encounter.highest_loot_modifier
        self.assertEqual(mod, self.encounter.get_loot_modifier())


class Monsters_And_CR_Tests(TestCase):
    """Tests for Challenge Rating and Monster Methods

    Args:
        TestCase (_type_): Django Test Module
    """

    def setUp(self):
        """Test Setup"""
        tag = Tag(Name="Infernal")
        tag.save()

        self.mon1 = Monster(
            Name="Fred",
            Description="A guy",
            Challenge_Rating=2.0,
            Strength=1,
            Dexterity=1,
            Constitution=1,
            Intelligence=1,
            Wisdom=1,
            Charisma=1,
        )
        self.mon2 = Monster(
            Name="Demon",
            Description="A demon",
            Challenge_Rating=10.0,
            Strength=1,
            Dexterity=1,
            Constitution=1,
            Intelligence=1,
            Wisdom=1,
            Charisma=1,
        )
        self.mon1.save()
        self.mon2.save()
        self.mon2.Creature_Tags.add(tag)

        self.encounter = enc_gen.Encounter_Generator()
        self.encounter.monster_list.append(self.mon1)
        self.encounter.tags.append(tag)

    def test_calculate_cr_positive(self):
        """Tests for calculate CR"""
        self.encounter.monster_list.append(self.mon1)
        self.encounter.calculate_average_cr()
        self.assertEqual(2, self.encounter.average_cr)

    def test_get_average_cr(self):
        """Tests for retrieve CR"""
        self.assertEqual(self.encounter.get_average_cr(), 0)

    def test_get_monster_list(self):
        """Tests for retrieve monster list"""
        a = [self.mon1]
        self.assertEqual(self.encounter.get_monster_list(), a)

    def test_monster_generate_positive(self):
        """Tests for generate monster"""
        self.encounter.average_party_level = 9
        self.encounter.generate_monster()
        self.assertIn(self.mon2, self.encounter.monster_list)

    def test_monster_generate_negative(self):
        """Tests for generate monster"""
        self.encounter.average_party_level = 20
        with self.assertRaises(RuntimeError):
            self.encounter.generate_monster()


class Generate_Test(TestCase):
    """Tests for generate encounter

    Args:
        TestCase (_type_): Django Test Module
    """

    def setUp(self):
        """Test setup"""
        self.encounter = enc_gen.Encounter_Generator()
        self.encounter1 = enc_gen.Encounter_Generator()
        self.encounter2 = enc_gen.Encounter_Generator()
        tag1 = Tag(Name="Infernal")
        tag2 = Tag(Name="Human")
        tag1.save()
        tag2.save()
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

        self.mon1 = Monster(
            Name="Fred",
            Description="A guy",
            Challenge_Rating=2.0,
            Strength=1,
            Dexterity=1,
            Constitution=1,
            Intelligence=1,
            Wisdom=1,
            Charisma=1,
            Gold_Modifier=1,
        )

        self.mon2 = Monster(
            Name="Demon",
            Description="A demon",
            Challenge_Rating=10.0,
            Strength=1,
            Dexterity=1,
            Constitution=1,
            Intelligence=1,
            Wisdom=1,
            Charisma=1,
            Gold_Modifier=10,
        )
        self.mon1.save()
        self.mon2.save()
        self.mon1.Creature_Tags.add(tag1)
        self.mon2.Creature_Tags.add(tag2)

    def test_generate_positive(self):
        """Test encounter generate method"""
        self.encounter1.generate_encounter()
        self.assertIn(self.mon1, self.encounter1.monster_list)
        self.encounter2.generate_encounter(average_level=9, loot_generate=True)
        self.assertIn(self.mon2, self.encounter2.monster_list)
        self.assertNotEqual(None, self.encounter2.dropped_loot)

    def test_generate_negative(self):
        with self.assertRaises(ValueError):
            self.encounter.generate_encounter(generator_key="Error")
        with self.assertRaises(ValueError):
            self.encounter.generate_encounter(loot_generate=3)
