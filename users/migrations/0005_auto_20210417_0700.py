# Generated by Django 3.2 on 2021-04-17 07:00

from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    dependencies = [
        ("users", "0004_auto_20210417_0453"),
    ]

    operations = [
        migrations.AlterField(
            model_name="city",
            name="country",
            field=models.ForeignKey(
                on_delete=django.db.models.deletion.CASCADE,
                related_name="cities",
                to="users.country",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="city",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="users.city",
            ),
        ),
        migrations.AlterField(
            model_name="user",
            name="country",
            field=models.ForeignKey(
                blank=True,
                null=True,
                on_delete=django.db.models.deletion.CASCADE,
                related_name="users",
                to="users.country",
            ),
        ),
    ]
