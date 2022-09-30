# Generated by Django 4.0.4 on 2022-09-20 01:21

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Account",
            fields=[
                (
                    "Email",
                    models.EmailField(
                        max_length=30, primary_key=True, serialize=False, unique=True
                    ),
                ),
                ("Username", models.CharField(max_length=15)),
                ("Password", models.CharField(max_length=20)),
            ],
        ),
    ]
