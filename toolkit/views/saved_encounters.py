from django.contrib import messages
from django.shortcuts import redirect, render
from django.views import View


class SavedEncounters(View):
    """A class to handle the retrieval and list of a user's saved encounters."""

    @staticmethod
    def get(request):
        """GET method for saved encounters page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        return render(request, "saved_encounters.html")

    @staticmethod
    def post(request):
        """POST method for saved encounters page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        return render(request, "saved_encounters.html")