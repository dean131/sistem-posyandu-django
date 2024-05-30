# Generated by Django 4.2.10 on 2024-05-29 11:42

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0033_rename_height_for_age_chart_growthchart_bmi_for_age_0_24_chart_and_more'),
    ]

    operations = [
        migrations.CreateModel(
            name='AnthropometricStandard',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('index', models.FloatField()),
                ('sd_minus_3', models.FloatField()),
                ('sd_minus_2', models.FloatField()),
                ('sd_minus_1', models.FloatField()),
                ('median', models.FloatField()),
                ('sd_plus_1', models.FloatField()),
                ('sd_plus_2', models.FloatField()),
                ('sd_plus_3', models.FloatField()),
                ('measurement_type', models.CharField(max_length=30)),
                ('gender', models.CharField(max_length=1)),
            ],
        ),
        migrations.DeleteModel(
            name='HeightForAgeBoys',
        ),
        migrations.DeleteModel(
            name='HeightForAgeGirls',
        ),
        migrations.DeleteModel(
            name='LengthForAgeBoys',
        ),
        migrations.DeleteModel(
            name='LengthForAgeGirls',
        ),
        migrations.DeleteModel(
            name='WeightForAgeBoys',
        ),
        migrations.DeleteModel(
            name='WeightForAgeGirls',
        ),
    ]
