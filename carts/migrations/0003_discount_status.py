# Generated by Django 3.2.6 on 2021-08-15 03:08

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('carts', '0002_delivery_postcode'),
    ]

    operations = [
        migrations.AddField(
            model_name='discount',
            name='status',
            field=models.PositiveSmallIntegerField(choices=[(1, 'Available'), (2, 'Expired')], default=1),
        ),
    ]
