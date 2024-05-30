# Generated by Django 4.2.10 on 2024-05-29 05:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0032_alter_childmeasurement_posyandu_activity'),
    ]

    operations = [
        migrations.RenameField(
            model_name='growthchart',
            old_name='height_for_age_chart',
            new_name='bmi_for_age_0_24_chart',
        ),
        migrations.RenameField(
            model_name='growthchart',
            old_name='legth_for_age_chart',
            new_name='bmi_for_age_24_60_chart',
        ),
        migrations.RenameField(
            model_name='growthchart',
            old_name='weight_for_age_chart_0_24',
            new_name='height_for_age_24_60_chart',
        ),
        migrations.RenameField(
            model_name='growthchart',
            old_name='weight_for_age_chart_24_60',
            new_name='legth_for_age_0_24_chart',
        ),
        migrations.AddField(
            model_name='growthchart',
            name='weight_for_age_0_24_chart',
            field=models.ImageField(blank=True, null=True, upload_to='growth_charts/'),
        ),
        migrations.AddField(
            model_name='growthchart',
            name='weight_for_age_24_60_chart',
            field=models.ImageField(blank=True, null=True, upload_to='growth_charts/'),
        ),
        migrations.AddField(
            model_name='growthchart',
            name='weight_for_length_chart',
            field=models.ImageField(blank=True, null=True, upload_to='growth_charts/'),
        ),
    ]
