# Generated by Django 3.2.16 on 2023-01-15 07:28

from django.conf import settings
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('products', '0002_basket'),
    ]

    operations = [
        migrations.RenameModel(
            old_name='Basket',
            new_name='BasketItem',
        ),
    ]
