import unittest

import character_generation as Char_Gen


class PositiveTests(unittest.TestCase):
    def test_generate_stats(self):
        test_stats = Char_Gen.Character_Generator.generate_stat_list("random")
        self.assertEqual(len(test_stats), 6)
        print(test_stats)
        for i in test_stats:
            self.assertTrue(type(i) is int)
            self.assertGreater(i, 0)
            self.assertLessEqual(i, 18)

        test_stats = Char_Gen.Character_Generator.generate_stat_list("random")
        print(test_stats)
        self.assertEqual(len(test_stats), 6)
        for i in test_stats:
            self.assertTrue(type(i) is int)
            self.assertGreater(i, 0)
            self.assertLessEqual(i, 18)

    def test_generate_race(self):
        test_race = Char_Gen.Character_Generator.generate_race(
            Char_Gen.Character_Generator.RACE_DICT["All"], "random"
        )
        print(test_race)
        self.assertTrue(test_race in Char_Gen.Character_Generator.RACE_DICT["All"])

        test_race = Char_Gen.Character_Generator.generate_race(
            Char_Gen.Character_Generator.RACE_DICT["Common"], "random"
        )
        print(test_race)
        self.assertTrue(test_race in Char_Gen.Character_Generator.RACE_DICT["Common"])

        test_race = Char_Gen.Character_Generator.generate_race(
            Char_Gen.Character_Generator.RACE_DICT["Monster"], "random"
        )
        print(test_race)
        self.assertTrue(test_race in Char_Gen.Character_Generator.RACE_DICT["Monster"])

        test_race = Char_Gen.Character_Generator.generate_race(
            Char_Gen.Character_Generator.RACE_DICT["Rare"], "random"
        )
        print(test_race)
        self.assertTrue(test_race in Char_Gen.Character_Generator.RACE_DICT["Rare"])

    def test_generate_class(self):
        test_class = Char_Gen.Character_Generator.generate_class(
            Char_Gen.Character_Generator.CLASS_DICT["All"], "random"
        )
        print(test_class)
        self.assertTrue(test_class in Char_Gen.Character_Generator.CLASS_DICT["All"])

        test_class = Char_Gen.Character_Generator.generate_class(
            Char_Gen.Character_Generator.CLASS_DICT["Martial"], "random"
        )
        print(test_class)
        self.assertTrue(
            test_class in Char_Gen.Character_Generator.CLASS_DICT["Martial"]
        )

        test_class = Char_Gen.Character_Generator.generate_class(
            Char_Gen.Character_Generator.CLASS_DICT["Magic"], "random"
        )
        print(test_class)
        self.assertTrue(test_class in Char_Gen.Character_Generator.CLASS_DICT["Magic"])

        test_class = Char_Gen.Character_Generator.generate_class(
            Char_Gen.Character_Generator.CLASS_DICT["Divine"], "random"
        )
        print(test_class)
        self.assertTrue(test_class in Char_Gen.Character_Generator.CLASS_DICT["Divine"])

    def test_generate_alignment(self):
        test_alignment = Char_Gen.Character_Generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["All"], "random"
        )
        print(test_alignment)
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["All"]
        )

        test_alignment = Char_Gen.Character_Generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["Good"], "random"
        )
        print(test_alignment)
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["Good"]
        )

        test_alignment = Char_Gen.Character_Generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["Neutral"], "random"
        )
        print(test_alignment)
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["Neutral"]
        )

        test_alignment = Char_Gen.Character_Generator.generate_alignment(
            Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"], "random"
        )
        print(test_alignment)
        self.assertTrue(
            test_alignment in Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"]
        )

    def test_generate_background(self):
        test_background = Char_Gen.Character_Generator.generate_background(
            Char_Gen.Character_Generator.BACKGROUND_LIST, "random"
        )
        print(test_background)
        self.assertTrue(test_background in Char_Gen.Character_Generator.BACKGROUND_LIST)

    def test_generate(self):
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
            ["Stats", "Alignment"], "Evil", [13, 13, 13, 13, 13, 13]
        )
        self.assertEqual(len(test_generated), 5)
        self.assertTrue(
            test_generated["Alignment"]
            in Char_Gen.Character_Generator.ALIGNMENT_DICT["Evil"]
        )
        for i in test_generated["Stats"]:
            self.assertTrue(type(i) is int)
            self.assertEqual(i, 13)


class Negative_Tests(unittest.TestCase):
    def test_generate_stats(self):
        with self.assertRaises(RuntimeError, msg="Should not except nonexisting keys"):
            Char_Gen.Character_Generator.generate_stat_list("GARBAGE")
        with self.assertRaises(Exception, msg="Should not except that many inputs"):
            Char_Gen.Character_Generator.generate_stat_list("random", "too many")
        with self.assertRaises(Exception, msg="Should not except that few inputs"):
            Char_Gen.Character_Generator.generate_stat_list()

    def test_generate_race(self):
        with self.assertRaises(RuntimeError, msg="Should not except nonexisting keys"):
            Char_Gen.Character_Generator.generate_race(
                Char_Gen.Character_Generator.RACE_DICT["All"], "GARBAGE"
            )
        with self.assertRaises(RuntimeError, msg="Should not except nonexisting keys"):
            Char_Gen.Character_Generator.generate_race(["Potato"], "random")
        with self.assertRaises(Exception, msg="Should not except that many inputs"):
            Char_Gen.Character_Generator.generate_stat_list(
                Char_Gen.Character_Generator.RACE_DICT["All"], "random", "too many"
            )
        with self.assertRaises(Exception, msg="Should not except that few inputs"):
            Char_Gen.Character_Generator.generate_stat_list(
                Char_Gen.Character_Generator.RACE_DICT["All"]
            )

    def test_generate_class(self):
        with self.assertRaises(RuntimeError, msg="Should not except nonexisting keys"):
            Char_Gen.Character_Generator.generate_class(
                Char_Gen.Character_Generator.CLASS_DICT["All"], "GARBAGE"
            )
        with self.assertRaises(
            RuntimeError, msg="Should not except nonapproved items in the list"
        ):
            Char_Gen.Character_Generator.generate_class(["Musician"], "random")
        with self.assertRaises(Exception, msg="Should not except that many inputs"):
            Char_Gen.Character_Generator.generate_class(
                Char_Gen.Character_Generator.CLASS_DICT["All"], "random", "too many"
            )
        with self.assertRaises(Exception, msg="Should not except that few inputs"):
            Char_Gen.Character_Generator.generate_class(
                Char_Gen.Character_Generator.CLASS_DICT["All"]
            )

    def test_generate_alignment(self):
        with self.assertRaises(RuntimeError, msg="Should not except nonexisting keys"):
            Char_Gen.Character_Generator.generate_alignment(
                Char_Gen.Character_Generator.ALIGNMENT_DICT["All"], "GARBAGE"
            )
        with self.assertRaises(
            RuntimeError, msg="Should not except nonapproved items in the list"
        ):
            Char_Gen.Character_Generator.generate_alignment(
                ["Chaotic Stupid"], "random"
            )
        with self.assertRaises(Exception, msg="Should not except that many inputs"):
            Char_Gen.Character_Generator.generate_alignment(
                Char_Gen.Character_Generator.ALIGNMENT_DICT["All"], "random", "too many"
            )
        with self.assertRaises(Exception, msg="Should not except that few inputs"):
            Char_Gen.Character_Generator.generate_alignment(
                Char_Gen.Character_Generator.ALIGNMENT_DICT["All"]
            )

    def test_generate_background(self):
        with self.assertRaises(RuntimeError, msg="Should not except nonexisting keys"):
            Char_Gen.Character_Generator.generate_background(
                Char_Gen.Character_Generator.BACKGROUND_LIST, "GARBAGE"
            )
        with self.assertRaises(
            RuntimeError, msg="Should not except nonapproved items in the list"
        ):
            tChar_Gen.Character_Generator.generate_background(["Adventurer"], "random")
        with self.assertRaises(Exception, msg="Should not except that many inputs"):
            Char_Gen.Character_Generator.generate_background(
                Char_Gen.Character_Generator.BACKGROUND_LIST, "random", "too many"
            )
        with self.assertRaises(Exception, msg="Should not except that few inputs"):
            Char_Gen.Character_Generator.generate_background(
                Char_Gen.Character_Generator.BACKGROUND_LIST
            )

    def test_generate(self):
        with self.assertRaises(ValueError, msg="Should not except such small arrays"):
            Char_Gen.Character_Generator.Generate([12, 12, 12, 12])
        with self.assertRaises(RuntimeError, msg="Should not except non integers"):
            Char_Gen.Character_Generator.Generate([12, 12, 12, 12, 12, "Test"])
        with self.assertRaises(
            RuntimeError, msg="Should not except such large numbers"
        ):
            Char_Gen.Character_Generator.Generate([12, 12, 12, 12, 12, 60])
        with self.assertRaises(Exception, msg="Should not except so many inputs"):
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
