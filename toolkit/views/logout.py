from django.contrib.auth import logout
from django.shortcuts import redirect
from django.views import View


class Logout(View):
    """View to handle logout requests started from user navbar dropdown selection."""

    @staticmethod
    def custom_logout(request):
        """Logout a user if they are logged in. Redirects back to home page."""
        logout(request)
        return redirect("home_page")
