# Generated by Django 5.1.2 on 2024-10-21 18:20

from django.db import migrations, models


class Migration(migrations.Migration):
    initial = True

    dependencies = []

    operations = [
        migrations.CreateModel(
            name="Stock",
            fields=[
                (
                    "id",
                    models.BigAutoField(
                        auto_created=True,
                        primary_key=True,
                        serialize=False,
                        verbose_name="ID",
                    ),
                ),
                ("stock_symbol", models.CharField(max_length=20)),
                ("open_price", models.DecimalField(decimal_places=3, max_digits=10)),
                ("close_price", models.DecimalField(decimal_places=3, max_digits=10)),
                ("high_price", models.DecimalField(decimal_places=3, max_digits=10)),
                ("low_price", models.DecimalField(decimal_places=3, max_digits=10)),
                ("time_stamp", models.DateTimeField()),
                ("volume", models.BigIntegerField()),
            ],
            options={
                "ordering": ["-low_price"],
                "unique_together": {("stock_symbol", "time_stamp")},
            },
        ),
    ]