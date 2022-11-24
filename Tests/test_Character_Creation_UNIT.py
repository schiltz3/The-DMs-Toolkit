import unittest

import django
from django.test import TestCase

import toolkit.views.character_generator.character_generator_backend as Char_Gen
from toolkit.models import Clazz, Race

django.setup()


class PositiveTests(TestCase):
    """Testing for positive results from various character generation classes"""

    def setUp(self):
        """Set up a generator for each test"""
        self.generator = Char_Gen.Character_Generator()

    def test_generate_stats(self):
        """Tests the Random stat generation method"""
        test_stats = self.generator.generate_stat_list("Random")
        self.assertEqual(len(test_stats), 6)
        for i in test_stats:
            self.assertTrue(type(i) is int)
            self.assertGreater(i, 0)
            self.assertLessEqual(i, 18)

        test_stats = self.generator.generate_stat_list("Random")
        self.assertEqual(len(test_stats), 6)
        for i in test_stats:
            self.assertTrue(type(i) is int)
            self.assertGreater(i, 0)
            self.assertLessEqual(i, 18)

    def test_generate_race(self):
        """Tests the generate race method"""
        Monster = Race(Name="A", Options="Monster", Speed=30)
        Monster.save()
        Common = Race(Name="B", Options="Common", Speed=30)
        Common.save()
        Rare = Race(Name="C", Options="Rare", Speed=30)
        Rare.save()
        test_race = self.generator.generate_race("All", "Random")
        self.assertTrue(test_race in Race.objects.all())

        test_race = self.generator.generate_race("Common", "Random")
        self.assertEqual(test_race, Common)

        test_race = self.generator.generate_race("Monster", "Random")
        self.assertEqual(test_race, Monster)

        test_race = self.generator.generate_race("Rare", "Random")
        self.assertEqual(test_race, Rare)

    def test_generate_class(self):
        """Tests the generate class method"""
        fighter = Clazz(
            Name="Fighter", Options="Martial", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        fighter.save()
        cleric = Clazz(
            Name="Cleric", Options="Divine", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        cleric.save()
        wizard = Clazz(
            Name="Wizard", Options="Magic", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        wizard.save()
        test_class = self.generator.generate_class("All", "Random")
        self.assertTrue(test_class in Clazz.objects.all())

        test_class = self.generator.generate_class("Martial", "Random")
        self.assertEqual(test_class, fighter)

        test_class = self.generator.generate_class("Divine", "Random")
        self.assertEqual(cleric, test_class)

        test_class = self.generator.generate_class("Magic", "Random")
        self.assertEqual(test_class, wizard)

    def test_generate_alignment(self):
        """Testing the generate alignment method"""
        test_alignment = self.generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["All"], "Random"
        )
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["All"]
        )

        test_alignment = self.generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["Good"], "Random"
        )
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["Good"]
        )

        test_alignment = self.generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["Neutral"], "Random"
        )
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["Neutral"]
        )

        test_alignment = self.generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"], "Random"
        )
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"]
        )

    def test_generate_background(self):
        """Testing the generate background function"""
        test_background = self.generator.generate_background(
            Char_Gen.Character_Generator.BACKGROUND_DICT["All"], "Random"
        )
        self.assertTrue(
            test_background in Char_Gen.Character_Generator.BACKGROUND_DICT["All"]
        )

    def test_generate(self):
        """_summary_"""
        Monster = Race(Name="A", Options="Monster", Speed=30)
        Monster.save()
        Common = Race(Name="B", Options="Common", Speed=30)
        Common.save()
        Rare = Race(Name="C", Options="Rare", Speed=30)
        Rare.save()
        fighter = Clazz(
            Name="Fighter", Options="Martial", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        fighter.save()
        cleric = Clazz(
            Name="Cleric", Options="Divine", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        cleric.save()
        wizard = Clazz(
            Name="Wizard", Options="Magic", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        wizard.save()
        # Testing the wider generate function
        test_generated = self.generator.generate()
        self.assertEqual(len(test_generated), 5)
        self.assertTrue(test_generated["Race"] in Race.objects.all())
        self.assertTrue(test_generated["Class"] in Clazz.objects.all())
        self.assertTrue(
            test_generated["Alignment"]
            in Char_Gen.Character_Generator.ALIGNMENT_DICT["All"]
        )
        self.assertTrue(
            test_generated["Background"]
            in Char_Gen.Character_Generator.BACKGROUND_DICT["All"]
        )
        for i in test_generated["Stats"]:
            self.assertTrue(type(i) is int)
            self.assertGreater(i, 0)
            self.assertLessEqual(i, 18)

        test_generated = self.generator.generate(["Race"])
        self.assertEqual(len(test_generated), 1)
        self.assertTrue(test_generated["Race"] in Race.objects.all())

        test_generated = self.generator.generate(
            ["Class", "Alignment", "Background", "Stats", "Race"],
            "Random",
            "Monster",
            "Magic",
            "Evil",
            "All",
            "Random",
            [12, 12, 12, 12, 12, 12],
        )
        self.assertEqual(len(test_generated), 5)
        self.assertTrue(test_generated["Race"] in Race.objects.all())
        self.assertTrue(test_generated["Class"] in Clazz.objects.all())
        self.assertTrue(
            test_generated["Alignment"]
            in Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"]
        )
        self.assertTrue(
            test_generated["Background"]
            in Char_Gen.Character_Generator.BACKGROUND_DICT["All"]
        )
        for i in test_generated["Stats"]:
            self.assertTrue(type(i) is int)
            self.assertEqual(i, 12)

        test_generated = self.generator.generate(
            generations_list=["Stats", "Alignment"],
            alignment_key="Evil",
            stat_list=[13, 13, 13, 13, 13, 13],
        )
        self.assertEqual(len(test_generated), 2)
        self.assertTrue(
            test_generated["Alignment"]
            in Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"]
        )
        for i in test_generated["Stats"]:
            self.assertTrue(type(i) is int)
            self.assertEqual(i, 13)


class Negative_Tests(TestCase):
    """Test the various cases where errors should be raised

    Args:
        unittest (_type_): _description_
    """

    def setUp(self):
        """Set up a generator for each test"""
        self.generator = Char_Gen.Character_Generator()

    def test_generate_stats(self):
        """
        Tests nonexisting keys
        Too many inputs
        Too few inputs
        """
        with self.assertRaises(RuntimeError, msg="Should not accept nonexisting keys"):
            self.generator.generate_stat_list("GARBAGE")
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            self.generator.generate_stat_list("Random", "too many")
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            self.generator.generate_stat_list()

    def test_generate_race(self):
        """
        Tests nonexisting keys
        Unapproved item in list
        Too many inputs
        Too few inputs
        """
        Monster = Race(Name="A", Options="Monster", Speed=30)
        Monster.save()
        Common = Race(Name="B", Options="Common", Speed=30)
        Common.save()
        Rare = Race(Name="C", Options="Rare", Speed=30)
        Rare.save()

        with self.assertRaises(
            RuntimeError, msg="Should not accept nonexisting race filters"
        ):
            self.generator.generate_race("Fighter", "GARBAGE")
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            self.generator.generate_stat_list("All", "Random", "too many")
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            self.generator.generate_stat_list("All")

    def test_generate_class(self):
        """
        Tests nonexisting keys
        Unapproved item in list
        Too many inputs
        Too few inputs
        """
        fighter = Clazz(
            Name="Fighter", Options="Martial", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        fighter.save()
        cleric = Clazz(
            Name="Cleric", Options="Divine", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        cleric.save()
        wizard = Clazz(
            Name="Wizard", Options="Magic", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        wizard.save()

        with self.assertRaises(RuntimeError, msg="Should not accept nonexisting keys"):
            self.generator.generate_class("Fighter", "GARBAGE")
        with self.assertRaises(
            RuntimeError, msg="Should not accept not in database item"
        ):
            self.generator.generate_class("Musician", "Random")
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            self.generator.generate_class("Fighter", "Random", "too many")
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            self.generator.generate_class("Fighter")

    def test_generate_alignment(self):
        """
        Tests nonexisting keys
        Unapproved item in list
        Too many inputs
        Too few inputs
        """
        with self.assertRaises(RuntimeError, msg="Should not accept nonexisting keys"):
            self.generator.generate_alignment(
                Char_Gen.Character_Generator.ALIGNMENT_DICT["All"], "GARBAGE"
            )
        with self.assertRaises(
            RuntimeError, msg="Should not accept nonapproved items in the list"
        ):
            self.generator.generate_alignment(["Chaotic Stupid"], "Random")
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            self.generator.generate_alignment(
                Char_Gen.Character_Generator.ALIGNMENT_DICT["All"], "Random", "too many"
            )
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            self.generator.generate_alignment(
                Char_Gen.Character_Generator.ALIGNMENT_DICT["All"]
            )

    def test_generate_background(self):
        """
        Tests nonexisting keys
        Unapproved item in list
        Too many inputs
        Too few inputs
        """
        with self.assertRaises(RuntimeError, msg="Should not accept nonexisting keys"):
            self.generator.generate_background(
                Char_Gen.Character_Generator.BACKGROUND_DICT["All"], "GARBAGE"
            )
        with self.assertRaises(
            RuntimeError, msg="Should not accept nonapproved items in the list"
        ):
            self.generator.generate_background(["Adventurer"], "Random")
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            self.generator.generate_background(
                Char_Gen.Character_Generator.BACKGROUND_DICT["All"],
                "Random",
                "too many",
            )
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            self.generator.generate_background(
                Char_Gen.Character_Generator.BACKGROUND_DICT["All"]
            )

    def test_generate(self):
        """
        Tests too small stat lists
        Unapproved item in list
        Tests too large stat numbers
        Too many inputs
        """
        with self.assertRaises(ValueError, msg="Should not accept such small arrays"):
            self.generator.generate(stat_list=[12, 12, 12, 12])
        with self.assertRaises(RuntimeError, msg="Should not accept non integers"):
            self.generator.generate(stat_list=[12, 12, 12, 12, 12, "Test"])
        with self.assertRaises(
            RuntimeError, msg="Should not accept such large numbers"
        ):
            self.generator.generate(stat_list=[12, 12, 12, 12, 12, 60])
        with self.assertRaises(Exception, msg="Should not accept so many inputs"):
            self.generator.generate(
                ["Class", "Alignment", "Background", "Stats", "Race"],
                "Random",
                "Monster",
                "Magic",
                "Evil",
                "All",
                "Random",
                [12, 12, 12, 12, 12, 12],
                "Test",
            )


class Arrange_Tests(unittest.TestCase):
    """
    Contains the various methods testing the arrange method for character creation

    Args:
        TestCase (_type_): Django Test Case
    """

    def setUp(self):
        """Set up a generator for each test"""
        self.generator = Char_Gen.Character_Generator()

    def test_positive_arrange(self):
        """Testing to make sure the arrange algorithm works"""
        Paladin = Clazz(
            Name="Paladin", Options="Divine", StatPrecedence="5,2,3,0,1,4", HitDice=10
        )
        Paladin.save()
        results = self.generator.arrange_stats("Paladin", [15, 10, 12, 13, 18, 9])
        self.assertEqual(results[0], 18)
        self.assertEqual(results[1], 12)
        self.assertEqual(results[2], 13)
        self.assertEqual(results[3], 9)
        self.assertEqual(results[4], 10)
        self.assertEqual(results[5], 15)

    def test_negative_arrange(self):
        """
        Test the rejected cases of the arrange method:
            Non existing character
            Too small stat array
            Too Big stat array
            Non integer in the stat array
        """

        with self.assertRaises(
            RuntimeError, msg="Should not accept a non existing class"
        ):
            self.generator.arrange_stats("Potato", [18, 16, 14, 12, 10, 8])
        with self.assertRaises(RuntimeError, msg="Should not accept a too small list"):
            self.generator.arrange_stats("Rogue", [18, 16, 14, 12, 10])
        with self.assertRaises(RuntimeError, msg="Should not accept a too big list"):
            self.generator.arrange_stats("Bard", [18, 16, 14, 12, 10, 8, 6, 4])
        with self.assertRaises(
            RuntimeError, msg="Should not accept a non integer in the list"
        ):
            self.generator.arrange_stats("Warlock", [18, 16, 14, 12, "Test"])
