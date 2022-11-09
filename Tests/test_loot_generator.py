from django.test import Client, TestCase
from django.urls import reverse

import toolkit.views.loot_generator.loot_generation as Loot_Gen
from toolkit.models import Armor, Weapon, GenericItem, MagicItem


class TestLootGenerator(TestCase):
    """Testing for loot generator page."""

    def setUp(self):
        """
        Function to set up all tests with information needed within
        each individual test case.
        """
        self.client = Client()
        self.loot_generator_url = reverse("loot_generator")
        self.loot_gen = Loot_Gen.Loot_Generator()
        
        
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
        
        self.generated_loot_object = self.loot_gen.generate_loot
        
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

    def test_successful_generate(self):
        """Tests if a user is able to successfully generate loot after giving correct input."""
        response = self.client.post(
            self.loot_generator_url,
            data={"total_value": self.username, "money": self.password},
            follow=True,
        )
        self.assertEqual(response.status_code, 200)


        
