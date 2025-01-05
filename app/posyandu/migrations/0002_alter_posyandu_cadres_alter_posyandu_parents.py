# Generated by Django 4.2.10 on 2025-01-05 13:39

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('posyandu', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posyandu',
            name='cadres',
            field=models.ManyToManyField(blank=True, related_name='cadre_posyandus', to='account.cadre'),
        ),
        migrations.AlterField(
            model_name='posyandu',
            name='parents',
            field=models.ManyToManyField(blank=True, related_name='parent_posyandus', to='account.parent'),
        ),
    ]