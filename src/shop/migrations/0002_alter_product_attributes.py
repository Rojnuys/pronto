# Generated by Django 5.1.2 on 2024-10-19 12:50

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="attributes",
            field=models.JSONField(blank=True, default=dict, verbose_name="attributes"),
        ),
    ]
