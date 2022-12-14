# Generated by Django 4.1 on 2022-09-29 18:08

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ("toolkit", "0003_user_alter_character_accountowner_delete_account"),
    ]

    operations = [
        migrations.AlterField(
            model_name="character",
            name="AccountOwner",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL
            ),
        ),
        migrations.DeleteModel(
            name="User",
        ),
    ]
