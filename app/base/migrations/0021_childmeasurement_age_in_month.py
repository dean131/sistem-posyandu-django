# Generated by Django 4.2.10 on 2024-05-03 08:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0020_remove_heightforageboys_title_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='childmeasurement',
            name='age_in_month',
            field=models.PositiveIntegerField(blank=True, null=True),
        ),
    ]
