# Generated by Django 5.1.6 on 2025-04-06 02:49

import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armory', '0011_rename_ammunition_id_issuedammunition_ammunition_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='watch',
            name='check_in',
            field=models.DateTimeField(default=django.utils.timezone.now),
            preserve_default=False,
        ),
        migrations.DeleteModel(
            name='IssuedAmmunition',
        ),
    ]
