# Generated by Django 4.2.10 on 2025-01-01 18:19

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0001_initial'),
        ('village', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='village',
            name='puskesmas',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='account.puskesmas'),
        ),
    ]
