# Generated by Django 4.2.10 on 2025-01-02 08:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('posyandu', '0002_alter_posyandu_parents'),
    ]

    operations = [
        migrations.AddField(
            model_name='posyandu',
            name='cadres',
            field=models.ManyToManyField(related_name='cadre_posyandus', to='account.cadre'),
        ),
        migrations.AlterField(
            model_name='posyandu',
            name='parents',
            field=models.ManyToManyField(related_name='posyandus', to='account.parent'),
        ),
    ]
