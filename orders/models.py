from django.contrib.auth.models import User
from django.db import models

from carts.models import Cart


class Order(models.Model):
    order_status_choices = (
        (1, 'Berjaya'),
        (2, 'Dalam Proses'),
        (3, 'Gagal'),
        (4, 'Sudah Dipos'),
    )
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    reference_number = models.CharField(max_length=50, null=True)
    status = models.PositiveSmallIntegerField(choices=order_status_choices, default=2)
    reason = models.TextField(null=True)
    bill_code = models.CharField(max_length=50, null=True)
    amount = models.IntegerField(null=True)
    transaction_time = models.DateTimeField(null=True, auto_now_add=True)

    def display_order_number(self):
        return f'PKB{self.id:09}'

    def get_billcode_url(self):
        if 'https://toyyibpay.com/' in self.bill_code:
            return self.bill_code
        else:
            return f'https://toyyibpay.com/{self.bill_code}'

    def display_amount(self):
        amount = self.amount / 100
        return amount

    def __str__(self):
        return self.reference_number


class Tracking(models.Model):
    order = models.OneToOneField(Order, on_delete=models.SET_NULL, null=True)
    number = models.CharField(max_length=30, blank=True, null=True)
    submitter = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)
    created_on = models.DateTimeField(auto_now=True)


class OrderSummary(Order):
    class Meta:
        proxy = True
        verbose_name = 'Order Summary'
        verbose_name_plural = 'Orders Summary'
