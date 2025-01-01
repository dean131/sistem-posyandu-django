# Generated by Django 4.2.10 on 2025-01-01 10:26

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('child', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='ChildMeasurement',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('weight', models.FloatField()),
                ('height', models.FloatField()),
                ('head_circumference', models.FloatField(null=True)),
                ('measurement_method', models.CharField(choices=[('STANDING', 'Standing'), ('SUPINE', 'Supine')], max_length=8, null=True)),
                ('age', models.CharField(blank=True, max_length=50, null=True)),
                ('age_in_month', models.PositiveIntegerField(blank=True, null=True)),
                ('weight_for_age', models.CharField(blank=True, default='normal', max_length=30, null=True)),
                ('z_score_weight_for_age', models.FloatField(blank=True, null=True)),
                ('height_for_age', models.CharField(blank=True, default='normal', max_length=30, null=True)),
                ('z_score_height_for_age', models.FloatField(blank=True, null=True)),
                ('weight_for_height', models.CharField(blank=True, default='normal', max_length=30, null=True)),
                ('z_score_weight_for_height', models.FloatField(blank=True, null=True)),
                ('weight_gain', models.FloatField(blank=True, null=True)),
                ('height_gain', models.FloatField(blank=True, null=True)),
                ('bmi_for_age', models.CharField(blank=True, default='normal', max_length=30, null=True)),
                ('z_score_bmi_for_age', models.FloatField(blank=True, null=True)),
                ('created_at', models.DateTimeField(auto_now_add=True)),
                ('updated_at', models.DateTimeField(auto_now=True)),
                ('child', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='child.child')),
            ],
            options={
                'ordering': ['-age_in_month'],
            },
        ),
    ]
