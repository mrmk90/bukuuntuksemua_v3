# Generated by Django 3.2.6 on 2021-08-18 03:29

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('orders', '0002_ordersummary'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='amount',
            field=models.IntegerField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='bill_code',
            field=models.URLField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='reason',
            field=models.TextField(null=True),
        ),
        migrations.AlterField(
            model_name='order',
            name='reference_number',
            field=models.CharField(max_length=50, null=True),
        ),
    ]
