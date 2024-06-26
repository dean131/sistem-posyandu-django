# Generated by Django 4.2.10 on 2024-05-02 08:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0013_heightforageboys_heightforagegirls'),
    ]

    operations = [
        migrations.AlterField(
            model_name='childmeasurement',
            name='height_for_age',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='childmeasurement',
            name='weight_for_age',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='childmeasurement',
            name='weight_for_height',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AlterField(
            model_name='childmeasurement',
            name='z_score_height_for_age',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='childmeasurement',
            name='z_score_weight_for_age',
            field=models.FloatField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='childmeasurement',
            name='z_score_weight_for_height',
            field=models.FloatField(blank=True, null=True),
        ),
    ]
