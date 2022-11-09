from django.shortcuts import render
from django.views import View


class EncounterGenerator(View):
    """
    A class to provide a page for users visiting the site to
    generate randomized encounters.
    """

    def get(self, request):
        """GET method for encounter generation page."""
        return render(request, "encounter_generator.html")
