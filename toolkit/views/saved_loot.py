from django.shortcuts import render, redirect
from django.contrib import messages
from django.views import View


class SavedLoot(View):
    """A class to handle the retrieval and list of a user's saved loot."""
    
    def get(self, request):
        """GET method for saved loot page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        return render(request, "saved_loot.html")
    
    def post(self, request):
        """POST method for saved loot page"""
        if not request.user.is_authenticated:
            messages.warning(request, "You must be logged in to access this page.")
            return redirect("login")
        return render(request, "saved_loot.html")