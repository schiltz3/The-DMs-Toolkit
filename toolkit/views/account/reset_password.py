from django.http.request import HttpRequest
from django.shortcuts import render
from django.views import View


class ResetPassword(View):
    """hehe"""

    def get(self, request: HttpRequest):
        """hehe"""
        return render(request, "reset_password.html")

    def post(self, request: HttpRequest):
        """hehe"""
        return render(request, "reset_password.html")
