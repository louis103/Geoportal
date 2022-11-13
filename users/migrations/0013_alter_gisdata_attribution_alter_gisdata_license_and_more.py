# Generated by Django 4.1.1 on 2022-11-03 08:15

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0012_alter_gisdata_attribution_alter_gisdata_organization'),
    ]

    operations = [
        migrations.AlterField(
            model_name='gisdata',
            name='attribution',
            field=models.CharField(blank=True, default='No Attribution for this dataset!', max_length=1000, null=True, verbose_name='Attribution'),
        ),
        migrations.AlterField(
            model_name='gisdata',
            name='license',
            field=models.TextField(blank=True, default='Not Specified.', null=True, verbose_name='License'),
        ),
        migrations.AlterField(
            model_name='gisdata',
            name='organization',
            field=models.CharField(blank=True, default='Lowa Geoportal!', max_length=1000, null=True, verbose_name='Organization'),
        ),
    ]
