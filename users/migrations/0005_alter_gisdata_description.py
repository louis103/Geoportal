# Generated by Django 4.1.1 on 2022-10-24 04:56

import ckeditor_uploader.fields
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0004_alter_gisdata_description_alter_gisdata_gis_data_key_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisdata',
            name='description',
            field=ckeditor_uploader.fields.RichTextUploadingField(blank=True, null=True, verbose_name='Description'),
        ),
    ]
