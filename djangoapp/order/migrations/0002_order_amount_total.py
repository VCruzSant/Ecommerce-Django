# Generated by Django 5.0.3 on 2024-03-15 17:59

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('order', '0001_initial'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='amount_total',
            field=models.PositiveIntegerField(default=0),
        ),
    ]