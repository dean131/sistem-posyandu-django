# Generated by Django 4.2.10 on 2024-03-05 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('account', '0004_alter_user_role_otp'),
    ]

    operations = [
        migrations.AlterField(
            model_name='otp',
            name='expired_at',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AlterField(
            model_name='otp',
            name='otp',
            field=models.CharField(blank=True, max_length=6, null=True),
        ),
    ]
