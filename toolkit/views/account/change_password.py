from django.http.request import HttpRequest
from django.shortcuts import redirect
from django.views import View


class ChangePassword(View):
    def __init__(self, **kwargs):
        super().__init__(kwargs)
        self.hehe = "https://r.mtdv.me/blog/posts/changepassword"

    def get(self, request: HttpRequest, **kwargs):
        return redirect(self.hehe)

    def post(self, request: HttpRequest, **kwargs):
        """POST method for confirm account creation page."""
        username = kwargs.get("username", "")
        return redirect(self.hehe)
