from django.shortcuts import render
from django.views import View
from ..models import Account


class Login(View):
    """
    A class to handle the login page's GET and POST requests. As well as retrieve
    a user's credentials from the Account database.
    """

    def get(self, request):
        """GET method for login page."""
        return render(request, "login.html")

    def post(self, request):
        """POST method for login page."""   
        return render(request, "login.html")
    
    def retrieve_user(self, email, password):
        """Function used to authenticate user credentials from login

        Args:
            email (String): Email input received from form
            password (String): Password input received from form

        Returns:
            Boolean: True if email and password are correct
                     False if user not found or email and password incorrect
        """
        try:
            user = Account.objects.get(email=email)
            isValid = (user.password == password)
        except Account.DoesNotExist:
            return False
        return isValid