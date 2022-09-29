from django.shortcuts import render
from django.views import View
import thedmstoolkit.character_generation
class CharacterGenerator(View):
    """
    A class to provide a  page for users visiting the site to
    generate characters.
    """

    def get(self, request):
        """GET method for the character generation."""
        return render(request, "character_generator.html")
