# Generated by Django 5.1.6 on 2025-03-04 03:32

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('armory', '0001_initial'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='watch',
            name='check_in',
        ),
        migrations.RemoveField(
            model_name='watch',
            name='check_out',
        ),
        migrations.AddField(
            model_name='watch',
            name='check_in_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='watch',
            name='check_out_time',
            field=models.DateTimeField(blank=True, null=True),
        ),
    ]
