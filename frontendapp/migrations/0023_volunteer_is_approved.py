# Generated by Django 3.0.5 on 2025-04-05 02:17

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontendapp', '0022_volunteer'),
    ]

    operations = [
        migrations.AddField(
            model_name='volunteer',
            name='is_approved',
            field=models.BooleanField(default=False),
        ),
    ]
