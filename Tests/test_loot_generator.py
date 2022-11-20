from django.test import Client, TestCase
from django.urls import reverse

from toolkit.models import Armor, GenericItem, MagicItem, User, Weapon, GeneratedLoot, Cache
from toolkit.views.loot_generator.loot_generator_view import GenerateLootInputs


class TestLootGenerator(TestCase):
    """Testing for loot generator page."""

    def setUp(self):
        """
        Function to set up all tests with information needed within
        each individual test case.
        """
        self.client = Client()
        self.form = GenerateLootInputs()
        self.username = "dummy"
        self.password = "password"
        self.test_user = User.objects.create(username=self.username)
        self.test_user.set_password(self.password)
        self.test_user.save()
        self.loot_generator_url = reverse("loot_generator")
        self.generator_type = "Random"
        self.loot_type = "Random"
        self.total_hoard_value = 10
        self.average_player_level = 10

        self.mitem = MagicItem(
            Name="Rope", Rarity="Common", Type="Trinket", Attuned=False
        )
        self.mitem.save()

        self.item = GenericItem(Name="Rope", Description="It's Rope", Base_Value=0.01)
        self.item.save()

        self.weapon = Weapon(
            Name="Axe",
            Damage_Type="Slashing",
            Damage_Die="1d12",
            Base_Value=1.2,
            Max_Range=5,
            Weight=10,
            Special_Characteristics=101000000,
        )
        self.weapon.save()

        self.armor = Armor(
            Name="Plate",
            Armor_Type="Heavy",
            Base_Value=2.1,
            Armor_Class_Change=2,
            Weight=50,
            Stealth=True,
        )
        self.armor.save()

    def tearDown(self):
        """Function to clean up test database after each individual test."""
        self.mitem.delete()
        self.item.delete()
        self.weapon.delete()
        self.armor.delete()
        self.test_user.delete()

    def test_can_access_loot_page(self):
        """Tests to see if a user is able to access the loot page."""
        response = self.client.get(
            self.loot_generator_url,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "loot_generator.html")

    def test_user_can_access_loot_page(self):
        """Tests to see if a user is able to access the loot page."""
        self.client.login(username=self.username, password=self.password)
        response = self.client.get(
            self.loot_generator_url,
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "loot_generator.html")

    def test_valid_form(self):
        """Tests to see if a user's input form is valid."""
        form = self.form.from_dict(
            {
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            }
        )
        self.assertTrue(form.is_valid())

    def test_valid_form_total_hoard_value_empty(self):
        """Tests to see if a user's input form is valid when given empty total hoard value."""
        form = self.form.from_dict(
            {
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": "",
                "average_player_level": self.average_player_level,
            }
        )
        self.assertTrue(form.is_valid())

    def test_valid_form_player_level_empty(self):
        """Tests to see if a user's input form is valid when given empty player level."""
        form = self.form.from_dict(
            {
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": "",
            }
        )
        self.assertTrue(form.is_valid())

    def test_invalid_form_generator_type(self):
        """Tests to see if a user's input form is valid when given bad generator_type."""
        form = self.form.from_dict(
            {
                "generator_type": "Nonsense",
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_form_loot_type(self):
        """Tests to see if a user's input form is valid when given bad loot_type."""
        form = self.form.from_dict(
            {
                "generator_type": self.generator_type,
                "loot_type": "Nonsense",
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_form_total_hoard_value(self):
        """Tests to see if a user's input form is valid when given less than zero total hoard value."""
        form = self.form.from_dict(
            {
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": -1,
                "average_player_level": self.average_player_level,
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_form_player_level_zero(self):
        """Tests to see if a user's input form is valid when given zero or less player level."""
        form = self.form.from_dict(
            {
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": 0,
            }
        )
        self.assertFalse(form.is_valid())

    def test_invalid_form_player_level_high(self):
        """Tests to see if a user's input form is valid when given 22 or higher player level."""
        form = self.form.from_dict(
            {
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": 22,
            }
        )
        self.assertFalse(form.is_valid())

    def test_unsuccessful_generate_generator_type(self):
        """Tests if a user is able to successfully generate loot after giving incorrect generator type input."""
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": "",
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            self.assertEqual(response.context["total_value"], 0)

    def test_unsuccessful_generate_loot_type(self):
        """Tests if a user is able to successfully generate loot after giving incorrect loot type input."""
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": self.generator_type,
                "loot_type": "",
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        with self.assertRaises(KeyError):
            self.assertEqual(response.context["total_value"], 0)

    def test_successful_generate_total_hoard_value(self):
        """Tests if a user is able to successfully generate loot after giving empty hoard value input."""
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": "",
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context["total_value"], 0)

    def test_successful_generate_average_player_level(self):
        """Tests if a user is able to successfully generate loot after giving empty level input."""
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": "",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context["total_value"], 0)

    def test_successful_generate_average_player_level_hoard_value(self):
        """Tests if a user is able to successfully generate loot after giving empty level input and hoard value."""
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": "",
                "average_player_level": "",
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context["total_value"], 0)

    def test_successful_generate(self):
        """Tests if a user is able to successfully generate loot after giving correct input."""
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context["total_value"], 0)
        
    def test_save_cache(self):
        """Tests to see if a user can save generated loot in it's cache to the database."""
        self.client.force_login(self.test_user)
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        response = self.client.post(
            self.loot_generator_url,
            data={
                "save_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["cached"])
        cache = Cache.objects.get(user=self.test_user)
        self.assertIsNone(cache.loot)
        self.assertIsNotNone(GeneratedLoot.objects.filter(Owner=self.test_user))
        
    def test_generate_cache(self):
        """Tests to see if a user can save generated loot to it's cache."""
        self.client.force_login(self.test_user)
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertTrue(response.context["cached"])
        cache = Cache.objects.get(user=self.test_user)
        self.assertIsNotNone(cache.loot)
        
    def test_save_not_logged_in(self):
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        response = self.client.post(
            self.loot_generator_url,
            data={
                "save_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["cached"])
        cache = Cache.objects.get(user=self.test_user)
        self.assertIsNone(cache.loot)

    def test_clear(self):
        """Tests to see if a user is able to click the clear button and reset all inputs."""
        response = self.client.post(
            self.loot_generator_url,
            data={
                "clear_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_clear_cache(self):
        """Tests to see if a user can clear generated loot in it's cache."""
        self.client.force_login(self.test_user)
        response = self.client.post(
            self.loot_generator_url,
            data={
                "generate_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        response = self.client.post(
            self.loot_generator_url,
            data={
                "clear_button": "",
                "generator_type": self.generator_type,
                "loot_type": self.loot_type,
                "total_hoard_value": self.total_hoard_value,
                "average_player_level": self.average_player_level,
            },
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertFalse(response.context["cached"])
        cache = Cache.objects.get(user=self.test_user)
        self.assertIsNone(cache.loot)