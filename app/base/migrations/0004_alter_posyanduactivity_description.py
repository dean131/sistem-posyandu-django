# Generated by Django 4.2.10 on 2024-04-06 10:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0003_rename_village_midwifeassignment_village'),
    ]

    operations = [
        migrations.AlterField(
            model_name='posyanduactivity',
            name='description',
            field=models.TextField(blank=True, null=True),
        ),
    ]
