# Generated by Django 4.1.1 on 2022-11-07 13:38

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0021_alter_gisdata_category_alter_gisdata_gis_data_type_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisdata',
            name='category',
            field=models.CharField(blank=True, choices=[('Gis', 'Gis'), ('Humanitarian', 'Humanitarian'), ('Climate', 'Climate'), ('Social', 'Social'), ('Society', 'Society'), ('Remote', 'Remote'), ('Research', 'Research'), ('Economy', 'Economy'), ('Demography', 'Demography'), ('Other', 'Other')], default='GIS', max_length=100, verbose_name='Category'),
        ),
        migrations.AlterField(
            model_name='profile',
            name='avatar',
            field=models.ImageField(default='https://gisdata-001.s3.amazonaws.com/media/default.webp', upload_to='profile_images'),
        ),
    ]
