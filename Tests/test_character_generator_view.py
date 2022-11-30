import logging

from django.test import Client, TestCase
from django.urls import reverse

from toolkit.models import Cache, Character, Clazz, Race, User
from toolkit.views.character_generator.character_elements import (
    GenerateCharacterInputs,
    GeneratedCharacterOutputs,
)


class TestCharacterGenerator(TestCase):
    """Testing for character generator page."""

    def setUp(self):
        """
        Function to set up all tests with information needed within
        each individual test case.
        """
        logging.disable(
            logging.CRITICAL
        )  # Disable logging so it doesn't print when running tests
        self.client = Client()
        self.form = GenerateCharacterInputs()
        self.no_output = GeneratedCharacterOutputs(
            strength=0,
            dexterity=0,
            constitution=0,
            intelligence=0,
            wisdom=0,
            charisma=0,
            proficiency=2,
        )
        self.username = "dummy"
        self.password = "password"
        self.name = "Test"
        self.test_user = User.objects.create(username=self.username)
        self.test_user.set_password(self.password)
        self.test_user.save()
        self.character_generator_url = reverse("character_generator")
        self.gen_keys = [
            "3D6",
            "Standard",
        ]
        self.all = "All"
        self.clazz = Clazz(
            Name="Fighter", Options="Martial", StatPrecedence="0,1,2,3,4,5", HitDice=8
        )
        self.clazz.save()
        self.race = Race(Name="A", Options="Monster", Speed=30)
        self.race.save()

    def tearDown(self):
        """Function to clean up test database after each individual test."""
        self.test_user.delete()
        self.race.delete()
        self.clazz.save()
        logging.disable(logging.NOTSET)  # Re-enable logging after running tests

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

    def test_form_valid(self):
        """Tests to see if the form is valid given all correct input"""
        form = self.form.from_dict(
            {
                "character_name": self.name,
                "player_name": "",
                "clazz": self.all,
                "background": self.all,
                "race": self.race,
                "alignment": self.all,
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            }
        )
        self.assertTrue(form.is_valid())

    def test_form_invalid_clazz(self):
        """Tests to see if the form is invalid given invalid clazz"""
        form = self.form.from_dict(
            {
                "character_name": "",
                "player_name": "",
                "clazz": "",
                "background": self.all,
                "race": self.all,
                "alignment": self.all,
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_background(self):
        """Tests to see if the form is invalid given invalid background"""
        form = self.form.from_dict(
            {
                "character_name": "",
                "player_name": "",
                "clazz": self.all,
                "background": "",
                "race": self.all,
                "alignment": self.all,
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_race(self):
        """Tests to see if the form is invalid given invalid race"""
        form = self.form.from_dict(
            {
                "character_name": "",
                "player_name": "",
                "clazz": self.all,
                "background": self.all,
                "race": "",
                "alignment": self.all,
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_alignment(self):
        """Tests to see if the form is invalid given invalid alignment"""
        form = self.form.from_dict(
            {
                "character_name": "",
                "player_name": "",
                "clazz": self.all,
                "background": self.all,
                "race": self.all,
                "alignment": "",
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_form_invalid_generator(self):
        """Tests to see if the form is invalid given invalid background"""
        form = self.form.from_dict(
            {
                "character_name": "",
                "player_name": "",
                "clazz": self.all,
                "background": self.all,
                "race": self.all,
                "alignment": self.all,
                "generator_type": "",
                "experience_points": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_successful_generate_3D6(self):
        """Tests if a user is able to successfully generate character for all correct input."""
        response = self.client.post(
            self.character_generator_url,
            data={
                "generate_button": "",
                "character_name": self.name,
                "player_name": "",
                "clazz": self.all,
                "background": self.all,
                "race": self.all,
                "alignment": self.all,
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        output: GeneratedCharacterOutputs = response.context["out"]
        self.assertNotEqual(output.strength, self.no_output.strength)

    def test_successful_generate_Standard(self):
        """Tests if a user is able to successfully generate character for all correct input."""
        response = self.client.post(
            self.character_generator_url,
            data={
                "generate_button": "",
                "character_name": self.name,
                "player_name": "",
                "clazz": self.all,
                "background": self.all,
                "race": self.all,
                "alignment": self.all,
                "generator_type": self.gen_keys[1],
                "experience_points": 0,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        output: GeneratedCharacterOutputs = response.context["out"]
        self.assertNotEqual(output.strength, self.no_output.strength)

    def test_unsuccessful_generate_character_clazz(self):
        """Tests if a user is able to successfully generate character for incorrect clazz input."""
        response = self.client.post(
            self.character_generator_url,
            data={
                "generate_button": "",
                "character_name": self.name,
                "player_name": "",
                "clazz": "",
                "background": self.all,
                "race": self.all,
                "alignment": self.all,
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        output: GeneratedCharacterOutputs = response.context["out"]
        self.assertEqual(output.strength, self.no_output.strength)

    def test_unsuccessful_generate_character_background(self):
        """Tests if a user is able to successfully generate character for incorrect background input."""
        response = self.client.post(
            self.character_generator_url,
            data={
                "generate_button": "",
                "character_name": self.name,
                "player_name": "",
                "clazz": self.all,
                "background": "",
                "race": self.all,
                "alignment": self.all,
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        output: GeneratedCharacterOutputs = response.context["out"]
        self.assertEqual(output.strength, self.no_output.strength)

    def test_unsuccessful_generate_character_race(self):
        """Tests if a user is able to successfully generate character for incorrect race input."""
        response = self.client.post(
            self.character_generator_url,
            data={
                "generate_button": "",
                "character_name": self.name,
                "player_name": "",
                "clazz": self.all,
                "background": self.all,
                "race": "",
                "alignment": self.all,
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        output: GeneratedCharacterOutputs = response.context["out"]
        self.assertEqual(output.strength, self.no_output.strength)

    def test_unsuccessful_generate_character_alignment(self):
        """Tests if a user is able to successfully generate character for incorrect alignment input."""
        response = self.client.post(
            self.character_generator_url,
            data={
                "generate_button": "",
                "character_name": self.name,
                "player_name": "",
                "clazz": self.all,
                "background": self.all,
                "race": self.all,
                "alignment": "",
                "generator_type": self.gen_keys[0],
                "experience_points": 0,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        output: GeneratedCharacterOutputs = response.context["out"]
        self.assertEqual(output.strength, self.no_output.strength)
