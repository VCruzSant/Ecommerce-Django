# Generated by Django 5.0.2 on 2024-02-29 22:30

from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
    ]

    operations = [
        migrations.CreateModel(
            name='Product',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('name', models.CharField(max_length=255)),
                ('description_short', models.TextField(max_length=255)),
                ('description_long', models.TextField()),
                ('image', models.ImageField(upload_to='product_images/%Y/%m/')),
                ('slug', models.SlugField(blank=True, default=None, max_length=255, null=True, unique=True)),
                ('price_marketing', models.FloatField()),
                ('price_marketing_promotional', models.FloatField(default=0)),
                ('type', models.CharField(choices=[('V', 'Variation'), ('S', 'Simple')], default='V', max_length=1)),
            ],
            options={
                'verbose_name': 'Product',
                'verbose_name_plural': 'Products',
            },
        ),
    ]
