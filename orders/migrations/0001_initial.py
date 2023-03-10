# Generated by Django 3.2.5 on 2021-08-02 12:56

from django.conf import settings
from django.db import migrations, models
import django.db.models.deletion


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
        ('carts', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Order',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('reference_number', models.CharField(max_length=50)),
                ('status', models.PositiveSmallIntegerField(choices=[(1, 'Berjaya'), (2, 'Dalam Proses'), (3, 'Gagal'), (4, 'Sudah Dipos')], default=2)),
                ('reason', models.TextField()),
                ('bill_code', models.URLField()),
                ('amount', models.IntegerField()),
                ('transaction_time', models.DateTimeField(auto_now_add=True, null=True)),
                ('cart', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='carts.cart')),
                ('user', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to=settings.AUTH_USER_MODEL)),
            ],
        ),
        migrations.CreateModel(
            name='Tracking',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('number', models.CharField(blank=True, max_length=30, null=True)),
                ('created_on', models.DateTimeField(auto_now=True)),
                ('order', models.OneToOneField(null=True, on_delete=django.db.models.deletion.SET_NULL, to='orders.order')),
                ('submitter', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
        ),
    ]
