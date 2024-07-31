# Generated by Django 4.2.2 on 2024-07-30 11:38

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("main", "0003_reviews_owner"),
    ]

    operations = [
        migrations.AlterField(
            model_name="appointment",
            name="doctor",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                to="main.doctors",
                verbose_name="врач",
            ),
        ),
    ]
