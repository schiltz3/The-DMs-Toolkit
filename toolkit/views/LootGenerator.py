from django.shortcuts import render
from django.views import View


class LootGenerator(View):
    """
    A class to provide a  page for users visiting the site to
    generate loot.
    """

    def get(self, request):
        """GET method for the loot generation."""
        return render(request, "loot_generator.html")
