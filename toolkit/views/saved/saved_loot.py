from django.contrib import messages
from django.http.request import HttpRequest
from django.shortcuts import redirect, render
from django.views import View

from toolkit.models import GeneratedLoot


class SavedLoot(View):
    """A class to handle the retrieval and list of a user's saved characters."""

    def __init__(self):
        super(SavedLoot, self).__init__()
        self.context: dict[str, any] = {}

    def get(self, request: HttpRequest):
        """GET method for saved loot page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")

        User = request.user
        self.context["loot_list"] = GeneratedLoot.objects.filter(Owner=User)
        return render(request, "saved_loot.html", self.context)

    def post(self, request: HttpRequest):
        """POST method for saved loot page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        User = request.user
        self.context["loot_list"] = GeneratedLoot.objects.filter(Owner=User)
        view = request.POST.get("View")
        delete = request.POST.get("Delete")
        if view is not None:
            pass
        elif delete is not None:
            try:
                pk = int(delete)
                check = GeneratedLoot.objects.filter(pk = pk, Owner = User).first()
                if check is not None:
                    check.delete()
                else:
                    messages.warning(
                    request, "The Loot you are trying to delete can not be found")
                
            except ValueError:
                messages.error(request, "Can not get access Loot's database key")
        return render(request, "saved_loot.html")
