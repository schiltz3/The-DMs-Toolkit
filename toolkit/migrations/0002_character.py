# Generated by Django 4.1.1 on 2022-09-26 21:40

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("toolkit", "0001_initial"),
    ]

    operations = [
        migrations.CreateModel(
            name="Character",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("Name", models.CharField(max_length=20)),
                ("Race", models.CharField(max_length=15)),
                ("Class", models.CharField(max_length=9)),
                ("Background", models.CharField(max_length=22)),
                ("Alignment", models.CharField(max_length=17)),
                ("Level", models.IntegerField()),
                ("Experience", models.IntegerField()),
                ("Strength", models.IntegerField()),
                ("Dexterity", models.IntegerField()),
                ("Constitution", models.IntegerField()),
                ("Intelligence", models.IntegerField()),
                ("Wisdom", models.IntegerField()),
                ("Charisma", models.IntegerField()),
                (
                    "AccountOwner",
                    models.ForeignKey(
                        on_delete=django.db.models.deletion.CASCADE,
                        to="toolkit.account",
                    ),
                ),
            ],
        ),
    ]
