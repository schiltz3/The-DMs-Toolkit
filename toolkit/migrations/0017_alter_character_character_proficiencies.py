# Generated by Django 4.1.1 on 2022-11-17 04:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('toolkit', '0016_proficiencies_alter_generatedencounter_average_cr_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='character',
            name='Character_Proficiencies',
            field=models.ManyToManyField(blank=True, default='', to='toolkit.proficiencies'),
        ),
    ]