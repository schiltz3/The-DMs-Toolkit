from django.shortcuts import render
from django.views import View


class TestHome(View):
    def get(self, request):
        return render(request, "test_home.html")
