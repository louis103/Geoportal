# Generated by Django 4.1.1 on 2022-11-04 16:20

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0017_alter_gisdata_spatial_extent'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisdata',
            name='img_icon_url',
            field=models.CharField(blank=True, choices=[('https://cdn-icons-png.flaticon.com/512/28/28814.png', 'ZIPFILE')], default='', max_length=1000, verbose_name='Icon Url'),
        ),
    ]
