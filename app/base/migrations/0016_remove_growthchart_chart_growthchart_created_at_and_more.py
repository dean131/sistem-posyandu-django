# Generated by Django 4.2.10 on 2024-05-03 06:31

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0015_growthchart'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='growthchart',
            name='chart',
        ),
        migrations.AddField(
            model_name='growthchart',
            name='created_at',
            field=models.DateTimeField(auto_now_add=True, null=True),
        ),
        migrations.AddField(
            model_name='growthchart',
            name='height_for_age_chart',
            field=models.ImageField(blank=True, null=True, upload_to='growth_charts/'),
        ),
        migrations.AddField(
            model_name='growthchart',
            name='legth_for_age_chart',
            field=models.ImageField(blank=True, null=True, upload_to='growth_charts/'),
        ),
        migrations.AddField(
            model_name='growthchart',
            name='updated_at',
            field=models.DateTimeField(auto_now=True),
        ),
        migrations.AddField(
            model_name='growthchart',
            name='weight_for_age_chart',
            field=models.ImageField(blank=True, null=True, upload_to='growth_charts/'),
        ),
        migrations.AddField(
            model_name='growthchart',
            name='weight_for_height_chart',
            field=models.ImageField(blank=True, null=True, upload_to='growth_charts/'),
        ),
        migrations.AddField(
            model_name='heightforageboys',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='heightforageboys',
            name='xlabel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='heightforageboys',
            name='ylabel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='heightforagegirls',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='heightforagegirls',
            name='xlabel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='heightforagegirls',
            name='ylabel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lengthforageboys',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lengthforageboys',
            name='xlabel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lengthforageboys',
            name='ylabel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lengthforagegirls',
            name='title',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lengthforagegirls',
            name='xlabel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
        migrations.AddField(
            model_name='lengthforagegirls',
            name='ylabel',
            field=models.CharField(blank=True, max_length=255, null=True),
        ),
    ]
