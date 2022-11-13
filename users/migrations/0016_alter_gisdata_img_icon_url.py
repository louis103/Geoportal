# Generated by Django 4.1.1 on 2022-11-04 16:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0015_alter_gisdata_category'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisdata',
            name='img_icon_url',
            field=models.CharField(blank=True, choices=[('ZIPFILE', 'https://cdn-icons-png.flaticon.com/512/28/28814.png'), ('CSV', 'https://upload.wikimedia.org/wikipedia/commons/c/c6/.csv_icon.svg'), ('EXCEL', 'https://upload.wikimedia.org/wikipedia/commons/thumb/8/8d/Microsoft_Excel_Logo_%282013-2019%29.svg/192px-Microsoft_Excel_Logo_%282013-2019%29.svg.png?20180217032706'), ('JSON', 'https://cdn-icons-png.flaticon.com/512/136/136443.png'), ('SHAPEFILE', 'https://upload.wikimedia.org/wikipedia/commons/thumb/0/08/Colorado_counties_until_November_15%2C_2001.svg/800px-Colorado_counties_until_November_15%2C_2001.svg.png?20070405225702'), ('GEOTIFF', 'https://visibleearth.nasa.gov/img/geotiff.png'), ('GEOJSON', 'https://static.thenounproject.com/png/3962382-200.png'), ('TIFF', 'https://cdn-icons-png.flaticon.com/512/29/29058.png'), ('7ZIP', 'https://upload.wikimedia.org/wikipedia/commons/thumb/4/41/Simple_Comic_7z.png/640px-Simple_Comic_7z.png'), ('PNG', 'https://icons.iconarchive.com/icons/icons8/windows-8/512/Files-Png-icon.png'), ('RAR FILE', 'https://encrypted-tbn0.gstatic.com/images?q=tbn:ANd9GcRLPqd4e8xWKGB_J13hrARNidyJ6u2KzM5CHCX9CRWXYg&s'), ('PDF', 'https://upload.wikimedia.org/wikipedia/commons/thumb/6/6c/PDF_icon.svg/1200px-PDF_icon.svg.png'), ('GZ', 'https://cdn-icons-png.flaticon.com/512/29/29620.png'), ('JPEG', 'https://static.thenounproject.com/png/3180095-200.png'), ('JPG', 'https://cdn-icons-png.flaticon.com/512/29/29264.png')], default='', max_length=1000, verbose_name='Icon Url'),
        ),
    ]