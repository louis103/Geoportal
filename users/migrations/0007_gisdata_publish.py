# Generated by Django 4.1.1 on 2022-10-29 15:29

from django.db import migrations, models
import django.utils.timezone


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0006_remove_gisdata_description_gisdata_metadata_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='gisdata',
            name='publish',
            field=models.DateTimeField(default=django.utils.timezone.now),
        ),
    ]
