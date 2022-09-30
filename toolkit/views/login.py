from django.contrib import messages
from django.contrib.auth import authenticate, login
from django.shortcuts import redirect, render
from django.views import View


class Login(View):
    """
    A class to handle the login page's GET and POST requests. As well as retrieve
    a user's credentials from the User database.
    """

    def get(self, request, **kwargs):
        """GET method for login page."""
        username = kwargs.get("username")
        context = {"username": username}
        return render(request, "login.html", context)

    def post(self, request):
        """POST method for login page."""
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect("home_page")
        messages.error(request, "Username or password is incorrect")
        return redirect("login")
