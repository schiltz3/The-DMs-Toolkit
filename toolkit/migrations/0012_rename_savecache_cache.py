# Generated by Django 4.1.1 on 2022-11-13 02:43

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("toolkit", "0011_alter_savecache_character"),
    ]

    operations = [
        migrations.RenameModel(
            old_name="SaveCache",
            new_name="Cache",
        ),
    ]
