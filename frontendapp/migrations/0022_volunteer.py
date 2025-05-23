# Generated by Django 3.0.5 on 2025-04-04 17:07

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('frontendapp', '0021_auto_20250404_1511'),
    ]

    operations = [
        migrations.CreateModel(
            name='Volunteer',
            fields=[
                ('id', models.AutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=100)),
                ('email', models.EmailField(max_length=254)),
                ('address', models.TextField()),
                ('city', models.CharField(max_length=50)),
                ('phone', models.CharField(max_length=10)),
                ('profile_pic', models.ImageField(blank=True, null=True, upload_to='volunteer_pics/')),
            ],
        ),
    ]
