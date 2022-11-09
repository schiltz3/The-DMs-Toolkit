from django.test import Client, TestCase
from django.urls import reverse

from toolkit.views.loot_generator.loot_generator import GenerateLootInputs
from toolkit.models import User, Armor, Weapon, GenericItem, MagicItem


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
        
        
        self.mitem = MagicItem(Name="Rope", Rarity="Common", Type="Trinket", Attuned=False)
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
        form = self.form.from_dict({"generator_type": self.generator_type, "loot_type": self.loot_type, "total_hoard_value": self.total_hoard_value, "average_player_level": self.average_player_level})
        self.assertTrue(form.is_valid())
        
    def test_invalid_form_generator_type(self):
        form = self.form.from_dict({"generator_type": "Nonsense", "loot_type": self.loot_type, "total_hoard_value": self.total_hoard_value, "average_player_level": self.average_player_level})
        self.assertFalse(form.is_valid())
        
    def test_invalid_form_loot_type(self):
        form = self.form.from_dict({"generator_type": self.generator_type, "loot_type": "Nonsense", "total_hoard_value": self.total_hoard_value, "average_player_level": self.average_player_level})
        self.assertFalse(form.is_valid())
        
    def test_invalid_form_total_hoard_value(self):
        form = self.form.from_dict({"generator_type": self.generator_type, "loot_type": self.loot_type, "total_hoard_value": 0, "average_player_level": self.average_player_level})
        self.assertFalse(form.is_valid())
        
    def test_invalid_form_total_hoard_value_empty(self):
        form = self.form.from_dict({"generator_type": self.generator_type, "loot_type": self.loot_type, "total_hoard_value": "", "average_player_level": self.average_player_level})
        self.assertFalse(form.is_valid())
        
    def test_invalid_form_player_level_empty(self):
        form = self.form.from_dict({"generator_type": self.generator_type, "loot_type": self.loot_type, "total_hoard_value": self.total_hoard_value, "average_player_level": ""})
        self.assertFalse(form.is_valid())
        
    def test_invalid_form_player_level_zero(self):
        form = self.form.from_dict({"generator_type": self.generator_type, "loot_type": self.loot_type, "total_hoard_value": self.total_hoard_value, "average_player_level": 0})
        self.assertFalse(form.is_valid())
        
    def test_invalid_form_player_level_high(self):
        form = self.form.from_dict({"generator_type": self.generator_type, "loot_type": self.loot_type, "total_hoard_value": self.total_hoard_value, "average_player_level": 22})
        self.assertFalse(self.form.is_valid())

    def test_successful_generate(self):
        """Tests if a user is able to successfully generate loot after giving correct input."""
        response = self.client.post(
            self.loot_generator_url,
            data={"generate_button": "", "generator_type": self.generator_type, "loot_type": self.loot_type, "total_hoard_value": self.total_hoard_value, "average_player_level": self.average_player_level},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
        self.assertNotEqual(response.context["total_value"], 0)
        self.assertNotEqual(response.context["generated_list"], [])

    # Will be further developed when save functionality is implemented
    def test_save(self):
        response = self.client.post(
            self.loot_generator_url,
            data={"save_button": "", "generator_type": self.generator_type, "loot_type": self.loot_type, "total_hoard_value": self.total_hoard_value, "average_player_level": self.average_player_level},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)

    def test_clear(self):
        response = self.client.post(
            self.loot_generator_url,
            data={"clear_button": "", "generator_type": self.generator_type, "loot_type": self.loot_type, "total_hoard_value": self.total_hoard_value, "average_player_level": self.average_player_level},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)
