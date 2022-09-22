"""thedmstoolkit URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path

from toolkit.views.bootstrap_test import BootstrapTest
from toolkit.views.CharacterGenerator import CharacterGenerator
from toolkit.views.create_account import CreateAccount
from toolkit.views.EncounterGenerator import EncounterGenerator
from toolkit.views.home_page import HomePage
from toolkit.views.login import Login
from toolkit.views.LootGenerator import LootGenerator
from toolkit.views.test_home import TestHome

urlpatterns = [
    path("admin/", admin.site.urls),
    # home page
    path("", HomePage.as_view(), name="home_page"),
    # login
    path("login/", Login.as_view(), name="login"),
    # test home
    # path("", TestHome.as_view(), name="test_home"),
    # Create Class
    path("create_account/", CreateAccount.as_view(), name="create_account"),
    # Character Generator
    path(
        "character_generator/", CharacterGenerator.as_view(), name="character_generator"
    ),
    # Encounter Generator
    path(
        "encounter_generator/", EncounterGenerator.as_view(), name="encounter_generator"
    ),
    # Loot Generator
    path("loot_generator/", LootGenerator.as_view(), name="loot_generator"),
    # test sites
    path("bootstrap_test/", BootstrapTest.as_view(), name="bootstrap_test"),
    # static files
    *static(settings.STATIC_URL, document_root=settings.STATIC_ROOT),
]
