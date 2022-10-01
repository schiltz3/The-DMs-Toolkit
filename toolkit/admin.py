from django.contrib import admin

# Register your models here.
from .models import User
from .models import Character

admin.site.register(Character)