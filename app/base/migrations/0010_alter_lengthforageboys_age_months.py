# Generated by Django 4.2.10 on 2024-05-02 04:53

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0009_lengthforageboys'),
    ]

    operations = [
        migrations.AlterField(
            model_name='lengthforageboys',
            name='age_months',
            field=models.PositiveSmallIntegerField(unique=True, verbose_name='Umur (bulan)'),
        ),
    ]