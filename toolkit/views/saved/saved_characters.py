from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from toolkit.models import Character


class SavedCharacters(View):
    """A class to handle the retrieval and list of a user's saved characters."""

    def __init__(self):
        super(SavedCharacters, self).__init__()
        self.context: dict[str, any] = {}

    def get(self, request: HttpRequest):
        """GET method for saved characters page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        User = request.user
        self.context["char_list"] = Character.objects.filter(Owner=User)
        return render(request, "saved_characters.html", self.context)

    @staticmethod
    def post(request: HttpRequest):
        """POST method for saved characters page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        if request.POST.get("Delete") is not None:
            pass
        if request.POST.get("Details") is not None:
            return render(request, "character_generator.html")
        return render(request, "saved_characters.html")
