# Generated by Django 4.2.10 on 2024-05-03 07:55

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('base', '0019_alter_growthchart_height_for_age_chart_and_more'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='heightforageboys',
            name='title',
        ),
        migrations.RemoveField(
            model_name='heightforageboys',
            name='xlabel',
        ),
        migrations.RemoveField(
            model_name='heightforageboys',
            name='ylabel',
        ),
        migrations.RemoveField(
            model_name='heightforagegirls',
            name='title',
        ),
        migrations.RemoveField(
            model_name='heightforagegirls',
            name='xlabel',
        ),
        migrations.RemoveField(
            model_name='heightforagegirls',
            name='ylabel',
        ),
        migrations.RemoveField(
            model_name='lengthforageboys',
            name='title',
        ),
        migrations.RemoveField(
            model_name='lengthforageboys',
            name='xlabel',
        ),
        migrations.RemoveField(
            model_name='lengthforageboys',
            name='ylabel',
        ),
        migrations.RemoveField(
            model_name='lengthforagegirls',
            name='title',
        ),
        migrations.RemoveField(
            model_name='lengthforagegirls',
            name='xlabel',
        ),
        migrations.RemoveField(
            model_name='lengthforagegirls',
            name='ylabel',
        ),
    ]