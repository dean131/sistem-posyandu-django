# Generated by Django 4.2.10 on 2025-01-03 18:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('child_measurement', '0002_alter_childmeasurement_head_circumference'),
    ]

    operations = [
        migrations.RenameField(
            model_name='growthchart',
            old_name='height_for_age_chart',
            new_name='height_for_age_24_60_chart',
        ),
        migrations.RenameField(
            model_name='growthchart',
            old_name='length_for_age_chart',
            new_name='length_for_age_0_24_chart',
        ),
        migrations.RenameField(
            model_name='growthchart',
            old_name='weight_for_height_chart',
            new_name='weight_for_height_24_60_chart',
        ),
        migrations.RenameField(
            model_name='growthchart',
            old_name='weight_for_length_chart',
            new_name='weight_for_length_0_24_chart',
        ),
        migrations.RemoveField(
            model_name='childmeasurement',
            name='bmi_for_age',
        ),
        migrations.RemoveField(
            model_name='childmeasurement',
            name='height_gain',
        ),
        migrations.RemoveField(
            model_name='childmeasurement',
            name='weight_for_height',
        ),
        migrations.RemoveField(
            model_name='childmeasurement',
            name='weight_gain',
        ),
        migrations.RemoveField(
            model_name='childmeasurement',
            name='z_score_bmi_for_age',
        ),
        migrations.RemoveField(
            model_name='childmeasurement',
            name='z_score_weight_for_height',
        ),
    ]
