from django.contrib import admin

# Register your models here.
from .models import Character, User

admin.site.register(Character)
