import random

from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.views import View


class ChangePassword(View):
    def __init__(self, **kwargs):
        """hehe"""
        super().__init__(**kwargs)
        self.hehes = [
            "https://r.mtdv.me/blog/posts/changepassword",
            "https://www.youtube.com/watch?v=TXK03FHVsHk",
            "https://gprivate.com/61ufx",
            "reset_password",
        ]

    def get_hehe(self) -> str:
        """get's a good string"""
        return self.hehes[random.randint(0, len(self.hehes) - 1)]

    def get(self, request: HttpRequest):
        """hehe"""
        return redirect(self.get_hehe())

    def post(self, request: HttpRequest):
        """hehe"""
        return redirect(self.get_hehe())
