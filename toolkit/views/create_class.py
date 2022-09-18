from django.shortcuts import render
from django.views import View


class CreateClass(View):
    def get(self, request):
        return render(request, "create_class.html")