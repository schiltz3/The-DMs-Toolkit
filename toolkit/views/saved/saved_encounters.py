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

    def post(self, request: HttpRequest):
        """POST method for saved encounter page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        User = request.user
        self.context["encounter_list"] = GeneratedEncounter.objects.filter(Owner=User)
        view = request.POST.get("View")
        delete = request.POST.get("Delete")
        if view is not None:
            pass
        elif delete is not None:
            try:
                pk = int(delete)
                check = GeneratedEncounter.objects.filter(pk = pk, Owner = User).first()
                if check is not None:
                    check.delete()
                else:
                    messages.warning(
                    request, "The Encounter you are trying to delete can not be found")
            except ValueError:
                messages.error(request, "Can not get access Encounter's database key")
        self.context["encounter_list"] = GeneratedEncounter.objects.filter(Owner=User)
        return render(request, "saved_encounters.html")
