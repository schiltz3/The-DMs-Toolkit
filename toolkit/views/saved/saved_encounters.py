from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from toolkit.models import GeneratedEncounter


class SavedEncounters(View):
    """A class to handle the retrieval and list of a user's saved characters."""

    def __init__(self):
        super(SavedEncounters, self).__init__()
        self.context: dict[str, any] = {}

    def get(self, request: HttpRequest):
        """GET method for saved encounter page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        User = request.user
        self.context["encounter_list"] = GeneratedEncounter.objects.filter(Owner=User)
        return render(request, "saved_encounters.html", self.context)

    @staticmethod
    def post(request: HttpRequest):
        """POST method for saved encounter page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        if request.POST.get("Delete") is not None:
            pass
        if request.POST.get("Details") is not None:
            return render(request, "encounter_generator.html")
        return render(request, "saved_encounters.html")
