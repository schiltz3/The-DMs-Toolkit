# Generated by Django 4.1.1 on 2022-11-20 21:46

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolkit', '0021_clazz_options_race_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='clazz',
            name='Name',
            field=models.CharField(default='Temp', max_length=20),
            preserve_default=False,
        ),
    ]