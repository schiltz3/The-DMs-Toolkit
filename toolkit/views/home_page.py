from django.shortcuts import render
from django.views import View


class HomePage(View):
    """
    A class to provide a landing page for users visiting the site.
    Allows users to navigate to the three generator pages.
    """

    @staticmethod
    def get(request):
        """GET method for home page."""
        return render(request, "home_page.html")
