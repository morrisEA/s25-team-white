# Generated by Django 4.2.19 on 2025-04-07 16:56

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("armory", "0004_alter_watch_check_in_alter_watch_check_out"),
    ]

    operations = [
        migrations.AddField(
            model_name="firearm",
            name="available",
            field=models.BooleanField(default=True),
        ),
    ]
