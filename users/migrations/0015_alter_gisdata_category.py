# Generated by Django 4.1.1 on 2022-11-04 12:01

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0014_sendmessage'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisdata',
            name='category',
            field=models.CharField(blank=True, choices=[('Gis', 'Gis'), ('Humanitarian', 'Humanitarian'), ('Climate Change', 'Climate Change'), ('Social Life', 'Social Life'), ('Society', 'Society'), ('Remote Sensing', 'Remote Sensing'), ('Research', 'Research'), ('Economy', 'Economy'), ('Demography', 'Demography')], default='GIS', max_length=100, verbose_name='Category'),
        ),
    ]
