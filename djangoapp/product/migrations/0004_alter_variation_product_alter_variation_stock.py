# Generated by Django 5.0.2 on 2024-03-01 13:55

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('product', '0003_alter_product_description_long_variation'),
    ]

    operations = [
        migrations.AlterField(
            model_name='variation',
            name='product',
            field=models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='variation', to='product.product'),
        ),
        migrations.AlterField(
            model_name='variation',
            name='stock',
            field=models.PositiveIntegerField(default=1),
        ),
    ]
