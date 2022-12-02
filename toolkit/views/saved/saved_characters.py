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

    def post(self, request: HttpRequest):
        """POST method for saved characters page"""
        print("GOT POST")
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        User = request.user
        self.context["char_list"] = Character.objects.filter(Owner=User)
        view = request.POST.get("View")
        if view is not None:
            try:
                pk = int(view)
                return redirect("character_generator", pk=pk)
            except ValueError:
                messages.error(request,"Can not get access character's database key")
            print(view)
        return render(request, "saved_characters.html", self.context)
