from django.test import Client, TestCase
from django.urls import reverse

from toolkit.models import (
    Cache,
    Character,
    User,
)
from toolkit.views.character_generator.character_elements import GenerateCharacterInputs, GeneratedCharacterOutputs
from toolkit.views.character_generator.character_generator_backend import Character_Generator


class TestCharacterGenerator(TestCase):
    """Testing for character generator page."""

    def setUp(self):
        """
        Function to set up all tests with information needed within
        each individual test case.
        """
        self.client = Client()
        self.form = GenerateCharacterInputs()
        self.username = "dummy"
        self.password = "password"
        self.name = "Test"
        self.test_user = User.objects.create(username=self.username)
        self.test_user.set_password(self.password)
        self.test_user.save()
        self.character_generator_url = reverse("character_generator")
        self.clazz_list = Character_Generator.get_classes()
        self.background_list = sorted(
            Character_Generator.BACKGROUND_DICT.get("All")
        )
        self.race_list = Character_Generator.get_races()
        self.alignment_list = sorted(
            Character_Generator.ALIGNMENT_DICT.get("All")
        )
        self.gen_keys = []
        self.gen_keys.append("Standard")
        self.gen_keys.append("3D6")
        self.gen_keys = sorted(self.gen_keys)

    def tearDown(self):
        """Function to clean up test database after each individual test."""
        self.test_user.delete()

    def test_can_access_character_page(self):
        """Tests to see if a user is able to access the character generator page."""
        response = self.client.get(
            self.character_generator_url,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "character_generator.html")

    def test_user_can_access_character_page(self):
        """Tests to see if a logged in user is able to access the character generator page."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            self.character_generator_url,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "character_generator.html")

    def test_form_valid_clazz(self):
        """Tests to see if the form is valid given all clazz options"""
        for clazz in self.clazz_list:
            form = self.form.from_dict(
                {
                    "character_name": self.name,
                    "player_name": "",
                    "clazz": clazz, 
                    "background": self.background_list[0],
                    "race": self.race_list[0],
                    "alignment": self.alignment_list[0], 
                    "generator_type": self.gen_keys[0], 
                    "experience_points": 0, 
                }
            )
            self.assertTrue(form.is_valid())
            
    def test_form_valid_background(self):
        """Tests to see if the form is valid given all background options"""
        for background in self.clazz_list:
            form = self.form.from_dict(
                {
                    "character_name": self.name,
                    "player_name": "",
                    "clazz": self.clazz_list[0], 
                    "background": background,
                    "race": self.race_list[0],
                    "alignment": self.alignment_list[0], 
                    "generator_type": self.gen_keys[0], 
                    "experience_points": 0, 
                }
            )
            self.assertTrue(form.is_valid())
            
    def test_form_valid_race(self):
        """Tests to see if the form is valid given all race options"""
        for race in self.race_list:
            form = self.form.from_dict(
                {
                    "character_name": self.name,
                    "player_name": "",
                    "clazz": self.clazz_list[0], 
                    "background": self.background_list[0],
                    "race": race,
                    "alignment": self.alignment_list[0], 
                    "generator_type": self.gen_keys[0], 
                    "experience_points": 0, 
                }
            )
            self.assertTrue(form.is_valid())

    def test_form_valid_alignment(self):
        """Tests to see if the form is valid given all alignment options"""
        for alignment in self.alignment_list:
            form = self.form.from_dict(
                {
                    "character_name": self.name,
                    "player_name": "",
                    "clazz": self.clazz_list[0], 
                    "background": self.background_list[0],
                    "race": self.race_list[0],
                    "alignment": alignment, 
                    "generator_type": self.gen_keys[0], 
                    "experience_points": 0, 
                }
            )
            self.assertTrue(form.is_valid())
            
    def test_form_valid_generator(self):
        """Tests to see if the form is valid given all generator type options"""
        for generator in self.gen_keys:
            form = self.form.from_dict(
                {
                    "character_name": self.name,
                    "player_name": "",
                    "clazz": self.clazz_list[0], 
                    "background": self.background_list[0],
                    "race": self.race_list[0],
                    "alignment": self.alignment_list[0], 
                    "generator_type": generator, 
                    "experience_points": 0, 
                }
            )
            self.assertTrue(form.is_valid())