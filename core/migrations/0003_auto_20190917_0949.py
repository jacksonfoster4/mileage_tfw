# Generated by Django 2.2.4 on 2019-09-17 16:49

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('core', '0002_auto_20190830_1755'),
    ]

    operations = [
        migrations.AlterField(
            model_name='entry',
            name='odo_end',
            field=models.FloatField(default=0),
        ),
        migrations.AlterField(
            model_name='entry',
            name='odo_start',
            field=models.FloatField(default=0),
        ),
    ]
