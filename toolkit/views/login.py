from django.shortcuts import redirect, render
from django.views import View
from models import Account


class Login(View):
    def get(self, request):
        return render(request, "login.html")

    def post(self, request):
        return render(request, "login.html")

    # Function used to retrieve User from given email address or username and validate password
    def retrieve_user():
        pass
