# Generated by Django 4.2.4 on 2024-05-05 07:06

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('store_app', '0015_product_old_carty'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='product',
            name='old_carty',
        ),
    ]
