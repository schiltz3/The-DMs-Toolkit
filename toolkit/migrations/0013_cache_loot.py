# Generated by Django 4.1.1 on 2022-11-16 19:53

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('toolkit', '0012_rename_savecache_cache'),
    ]

    operations = [
        migrations.AddField(
            model_name='cache',
            name='loot',
            field=models.OneToOneField(blank=True, null=True, on_delete=django.db.models.deletion.CASCADE, to='toolkit.generatedloot'),
        ),
    ]
