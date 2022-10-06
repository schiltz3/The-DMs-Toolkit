import unittest

import django
from django.test import TestCase

import toolkit.views.character_generator.character_generation as Char_Gen
from toolkit.models import Character, User

django.setup()


class PositiveTests(TestCase):
    """Testing for positive results from various character generation classes"""

    def test_generate_stats(self):
        """Tests the random stat generation method"""
        test_stats = Char_Gen.Character_Generator.generate_stat_list("random")
        self.assertEqual(len(test_stats), 6)
        for i in test_stats:
            self.assertTrue(type(i) is int)
            self.assertGreater(i, 0)
            self.assertLessEqual(i, 18)

        test_stats = Char_Gen.Character_Generator.generate_stat_list("random")
        self.assertEqual(len(test_stats), 6)
        for i in test_stats:
            self.assertTrue(type(i) is int)
            self.assertGreater(i, 0)
            self.assertLessEqual(i, 18)

    def test_generate_race(self):
        """Tests the generate race method"""
        test_race = Char_Gen.Character_Generator.generate_race(
            Char_Gen.Character_Generator.RACE_DICT["All"], "random"
        )
        self.assertTrue(test_race in Char_Gen.Character_Generator.RACE_DICT["All"])

        test_race = Char_Gen.Character_Generator.generate_race(
            Char_Gen.Character_Generator.RACE_DICT["Common"], "random"
        )
        self.assertTrue(test_race in Char_Gen.Character_Generator.RACE_DICT["Common"])

        test_race = Char_Gen.Character_Generator.generate_race(
            Char_Gen.Character_Generator.RACE_DICT["Monster"], "random"
        )
        self.assertTrue(test_race in Char_Gen.Character_Generator.RACE_DICT["Monster"])

        test_race = Char_Gen.Character_Generator.generate_race(
            Char_Gen.Character_Generator.RACE_DICT["Rare"], "random"
        )
        self.assertTrue(test_race in Char_Gen.Character_Generator.RACE_DICT["Rare"])

    def test_generate_class(self):
        """Tests the generate class method"""
        test_class = Char_Gen.Character_Generator.generate_class(
            Char_Gen.Character_Generator.CLASS_DICT["All"], "random"
        )
        self.assertTrue(test_class in Char_Gen.Character_Generator.CLASS_DICT["All"])

        test_class = Char_Gen.Character_Generator.generate_class(
            Char_Gen.Character_Generator.CLASS_DICT["Martial"], "random"
        )
        self.assertTrue(
            test_class in Char_Gen.Character_Generator.CLASS_DICT["Martial"]
        )

        test_class = Char_Gen.Character_Generator.generate_class(
            Char_Gen.Character_Generator.CLASS_DICT["Magic"], "random"
        )
        self.assertTrue(test_class in Char_Gen.Character_Generator.CLASS_DICT["Magic"])

        test_class = Char_Gen.Character_Generator.generate_class(
            Char_Gen.Character_Generator.CLASS_DICT["Divine"], "random"
        )
        self.assertTrue(test_class in Char_Gen.Character_Generator.CLASS_DICT["Divine"])

    def test_generate_alignment(self):
        """Testing the generate alignment method"""
        test_alignment = Char_Gen.Character_Generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["All"], "random"
        )
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["All"]
        )

        test_alignment = Char_Gen.Character_Generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["Good"], "random"
        )
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["Good"]
        )

        test_alignment = Char_Gen.Character_Generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["Neutral"], "random"
        )
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["Neutral"]
        )

        test_alignment = Char_Gen.Character_Generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"], "random"
        )
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"]
        )

    def test_generate_background(self):
        """Testing the generate background function"""
        test_background = Char_Gen.Character_Generator.generate_background(
            Char_Gen.Character_Generator.BACKGROUND_LIST, "random"
        )
        self.assertTrue(test_background in Char_Gen.Character_Generator.BACKGROUND_LIST)

    def test_generate(self):
        """Testing the wider generate function"""
        test_generated = Char_Gen.Character_Generator.Generate()
        self.assertEqual(len(test_generated), 5)
        self.assertTrue(
            test_generated["Race"] in Char_Gen.Character_Generator.RACE_DICT["All"]
        )
        self.assertTrue(
            test_generated["Class"] in Char_Gen.Character_Generator.CLASS_DICT["All"]
        )
        self.assertTrue(
            test_generated["Alignment"]
            in Char_Gen.Character_Generator.ALIGNMENT_DICT["All"]
        )
        self.assertTrue(
            test_generated["Background"] in Char_Gen.Character_Generator.BACKGROUND_LIST
        )
        for i in test_generated["Stats"]:
            self.assertTrue(type(i) is int)
            self.assertGreater(i, 0)
            self.assertLessEqual(i, 18)

        test_generated = Char_Gen.Character_Generator.Generate(["Race"])
        self.assertEqual(len(test_generated), 1)
        self.assertTrue(
            test_generated["Race"] in Char_Gen.Character_Generator.RACE_DICT["All"]
        )

        test_generated = Char_Gen.Character_Generator.Generate(
            ["Class", "Alignment", "Background", "Stats", "Race"],
            "random",
            "Monster",
            "Magic",
            "Evil",
            "random",
            [12, 12, 12, 12, 12, 12],
        )
        self.assertEqual(len(test_generated), 5)
        self.assertTrue(
            test_generated["Race"] in Char_Gen.Character_Generator.RACE_DICT["Monster"]
        )
        self.assertTrue(
            test_generated["Class"] in Char_Gen.Character_Generator.CLASS_DICT["Magic"]
        )
        self.assertTrue(
            test_generated["Alignment"]
            in Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"]
        )
        self.assertTrue(
            test_generated["Background"] in Char_Gen.Character_Generator.BACKGROUND_LIST
        )
        for i in test_generated["Stats"]:
            self.assertTrue(type(i) is int)
            self.assertEqual(i, 12)

        test_generated = Char_Gen.Character_Generator.Generate(
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

    def test_generate_stats(self):
        """
        Tests nonexisting keys
        Too many inputs
        Too few inputs
        """
        with self.assertRaises(RuntimeError, msg="Should not accept nonexisting keys"):
            Char_Gen.Character_Generator.generate_stat_list("GARBAGE")
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            Char_Gen.Character_Generator.generate_stat_list("random", "too many")
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            Char_Gen.Character_Generator.generate_stat_list()

    def test_generate_race(self):
        """
        Tests nonexisting keys
        Unapproved item in list
        Too many inputs
        Too few inputs
        """
        with self.assertRaises(RuntimeError, msg="Should not accept nonexisting keys"):
            Char_Gen.Character_Generator.generate_race(
                Char_Gen.Character_Generator.RACE_DICT["All"], "GARBAGE"
            )
        with self.assertRaises(
            RuntimeError, msg="Should not accept unapproved items in lists"
        ):
            Char_Gen.Character_Generator.generate_race(["Potato"], "random")
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            Char_Gen.Character_Generator.generate_stat_list(
                Char_Gen.Character_Generator.RACE_DICT["All"], "random", "too many"
            )
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            Char_Gen.Character_Generator.generate_stat_list(
                Char_Gen.Character_Generator.RACE_DICT["All"]
            )

    def test_generate_class(self):
        """
        Tests nonexisting keys
        Unapproved item in list
        Too many inputs
        Too few inputs
        """
        with self.assertRaises(RuntimeError, msg="Should not accept nonexisting keys"):
            Char_Gen.Character_Generator.generate_class(
                Char_Gen.Character_Generator.CLASS_DICT["All"], "GARBAGE"
            )
        with self.assertRaises(
            RuntimeError, msg="Should not accept nonapproved items in the list"
        ):
            Char_Gen.Character_Generator.generate_class(["Musician"], "random")
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            Char_Gen.Character_Generator.generate_class(
                Char_Gen.Character_Generator.CLASS_DICT["All"], "random", "too many"
            )
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            Char_Gen.Character_Generator.generate_class(
                Char_Gen.Character_Generator.CLASS_DICT["All"]
            )

    def test_generate_alignment(self):
        """
        Tests nonexisting keys
        Unapproved item in list
        Too many inputs
        Too few inputs
        """
        with self.assertRaises(RuntimeError, msg="Should not accept nonexisting keys"):
            Char_Gen.Character_Generator.generate_alignment(
                Char_Gen.Character_Generator.ALIGNMENT_DICT["All"], "GARBAGE"
            )
        with self.assertRaises(
            RuntimeError, msg="Should not accept nonapproved items in the list"
        ):
            Char_Gen.Character_Generator.generate_alignment(
                ["Chaotic Stupid"], "random"
            )
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            Char_Gen.Character_Generator.generate_alignment(
                Char_Gen.Character_Generator.ALIGNMENT_DICT["All"], "random", "too many"
            )
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            Char_Gen.Character_Generator.generate_alignment(
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
            Char_Gen.Character_Generator.generate_background(
                Char_Gen.Character_Generator.BACKGROUND_LIST, "GARBAGE"
            )
        with self.assertRaises(
            RuntimeError, msg="Should not accept nonapproved items in the list"
        ):
            Char_Gen.Character_Generator.generate_background(["Adventurer"], "random")
        with self.assertRaises(Exception, msg="Should not accept that many inputs"):
            Char_Gen.Character_Generator.generate_background(
                Char_Gen.Character_Generator.BACKGROUND_LIST, "random", "too many"
            )
        with self.assertRaises(Exception, msg="Should not accept that few inputs"):
            Char_Gen.Character_Generator.generate_background(
                Char_Gen.Character_Generator.BACKGROUND_LIST
            )

    def test_generate(self):
        """
        Tests too small stat lists
        Unapproved item in list
        Tests too large stat numbers
        Too many inputs
        """
        with self.assertRaises(ValueError, msg="Should not accept such small arrays"):
            Char_Gen.Character_Generator.Generate(stat_list=[12, 12, 12, 12])
        with self.assertRaises(RuntimeError, msg="Should not accept non integers"):
            Char_Gen.Character_Generator.Generate(
                stat_list=[12, 12, 12, 12, 12, "Test"]
            )
        with self.assertRaises(
            RuntimeError, msg="Should not accept such large numbers"
        ):
            Char_Gen.Character_Generator.Generate(stat_list=[12, 12, 12, 12, 12, 60])
        with self.assertRaises(Exception, msg="Should not accept so many inputs"):
            Char_Gen.Character_Generator.Generate(
                ["Class", "Alignment", "Background", "Stats", "Race"],
                "random",
                "Monster",
                "Magic",
                "Evil",
                "random",
                [12, 12, 12, 12, 12, 12],
                "Test",
            )


class Arrange_Tests(unittest.TestCase):
    """
    Contains the various methods testing the arrange method for character creation

    Args:
        TestCase (_type_): Django Test Case
    """

    def test_positive_arrange(self):
        """Testing to make sure the arrange algorithm works"""
        tempUser = User(username="Ronen", password="test", email="test@test.com")
        tempUser.save()
        tempCharacter = Character(
            Name="Fred",
            AccountOwner=User.objects.get(username="Ronen"),
            Race="Human",
            Class="Rogue",
            Background="Sailor",
            Alignment="Chaotic Evil",
            Level=1,
            Experience=0,
            Strength=1,
            Dexterity=1,
            Constitution=1,
            Intelligence=1,
            Wisdom=1,
            Charisma=1,
        )
        tempCharacter.save()

        testChar = Character.objects.get(Name="Fred")
        Char_Gen.Character_Generator.Arrange(testChar.id, [18, 16, 14, 12, 10, 8])
        testChar = Character.objects.get(Name="Fred")
        self.assertEqual(testChar.Strength, 8)
        self.assertEqual(testChar.Dexterity, 18)
        self.assertEqual(testChar.Constitution, 16)
        self.assertEqual(testChar.Intelligence, 14)
        self.assertEqual(testChar.Wisdom, 10)
        self.assertEqual(testChar.Charisma, 12)

    def test_negative_arrange(self):
        """
        Test the rejected cases of the arrange method:
            Non existing character
            Too small stat array
            Too Big stat array
            Non integer in the stat array
        """
        tempUser = User(username="Ronen2", password="test", email="test@test.com")
        tempUser.save()
        tempCharacter = Character(
            Name="Fred2",
            AccountOwner=User.objects.get(username="Ronen2"),
            Race="Human",
            Class="Rogue",
            Background="Sailor",
            Alignment="Chaotic Evil",
            Level=1,
            Experience=0,
            Strength=1,
            Dexterity=1,
            Constitution=1,
            Intelligence=1,
            Wisdom=1,
            Charisma=1,
        )
        tempCharacter.save()
        testChar = Character.objects.get(Name="Fred2")
        with self.assertRaises(
            RuntimeError, msg="Should not accept a non existing character"
        ):
            Char_Gen.Character_Generator.Arrange(10, [18, 16, 14, 12, 10, 8])
        testChar = Character.objects.get(Name="Fred2")
        with self.assertRaises(RuntimeError, msg="Should not accept a too small list"):
            Char_Gen.Character_Generator.Arrange(testChar.id, [18, 16, 14, 12, 10])
        with self.assertRaises(RuntimeError, msg="Should not accept a too big list"):
            Char_Gen.Character_Generator.Arrange(
                testChar.pk, [18, 16, 14, 12, 10, 8, 6, 4]
            )
        with self.assertRaises(
            RuntimeError, msg="Should not accept a non integer in the list"
        ):
            Char_Gen.Character_Generator.Arrange(testChar.pk, [18, 16, 14, 12, "Test"])
        self.tearDown()
