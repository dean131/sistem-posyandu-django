# Generated by Django 4.2.10 on 2024-05-02 04:14

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0007_parentposyandu'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childmeasurement',
            name='age',
            field=models.CharField(blank=True, max_length=50, null=True),
        ),
    ]
