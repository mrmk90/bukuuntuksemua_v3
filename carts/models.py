from decimal import Decimal

from django.contrib.auth.models import User
from django.db import models
from django.db.models import F
from django.db.models import Sum
from django.db.models.functions import Coalesce
from djmoney.money import Money

from books.models import Book


class Discount(models.Model):
    AVAILABLE = 1
    EXPIRED = 2
    status_choices = (
        (AVAILABLE, 'Available'),
        (EXPIRED, 'Expired'),
    )
    code = models.CharField(max_length=20)
    discount = models.DecimalField(max_digits=3, decimal_places=2)
    status = models.PositiveSmallIntegerField(choices=status_choices, default=AVAILABLE)

    def __str__(self):
        return f'{self.code}'


class Delivery(models.Model):
    name = models.CharField(max_length=100)
    address = models.TextField()
    postcode = models.CharField(max_length=7)
    state = models.CharField(max_length=20)
    phone_number = models.CharField(max_length=15)


class Cart(models.Model):
    NEW = 0
    OLD = 1
    status_choices = (
        (NEW, 'New'),
        (OLD, 'Old')
    )
    created_on = models.DateTimeField(auto_now=True)
    user = models.ForeignKey(User, on_delete=models.CASCADE)
    status = models.PositiveSmallIntegerField(choices=status_choices)
    discount = models.ForeignKey(Discount, on_delete=models.SET_NULL, null=True)
    delivery = models.OneToOneField(Delivery, on_delete=models.SET_NULL, null=True)

    def __str__(self):
        return f'Cart {self.id} created on {self.created_on}.'

    def get_total_quantity_cart_item(self):
        return self.cartitem_set.all().aggregate(total=Coalesce(Sum('quantity'), 0))['total']

    def get_total_book_price(self):
        total = self.cartitem_set.all().aggregate(
            total=Coalesce(Sum(F('quantity') * F('item__price')), Decimal('0.00'))
        )['total']
        return Money(total, 'MYR')

    def get_discount_amount(self):
        total_book_price = self.get_total_book_price()
        if self.discount and self.discount.code in ('baucarBOCA',):  # diskaun RM10 untuk pembelian melebihi RM50
            if total_book_price >= Money('30.00', 'MYR'):
                return Money('10.00', 'MYR')
            else:
                return Money('0.00', 'MYR')
        elif self.discount and self.discount.code in ('BocaPBS',): # diskaun RM 10 untuk pembelian melebihi RM 30
            if total_book_price >= Money('30.00', 'MYR'):
                return Money('10.00', 'MYR')
            else:
                return Money('0.00', 'MYR')
        elif self.discount and self.discount.code in ('BaucarBOCA',):  # diskaun RM20 atau max harga total buku
            diskaun = Money('20.00', 'MYR')
            return min(diskaun, total_book_price)
        elif self.discount and self.discount.code in ('SembangMerdeka',):
            diskaun = Money('10.00', 'MYR')
            return min(diskaun, total_book_price)
        elif self.discount:
            return total_book_price * self.discount.discount
        else:
            return Money('0.00', 'MYR')

    def get_total_book_price_with_discount(self):
        if self.get_total_book_price() < self.get_discount_amount():
            return Money('0.00', 'MYR')
        else:
            return self.get_total_book_price() - self.get_discount_amount()

    def get_delivery_cost(self):
        # Free Delivery Baucar
        if self.discount and self.discount.code == 'PosPercumaDiBOCA':
            return Money(0.00, decimal_places=2, currency='MYR')

        if self.delivery and self.delivery.state in ('Sabah', 'Sarawak', 'Labuan'):
            return Money(18.00, decimal_places=2, currency='MYR')
        else:
            return Money(8.00, decimal_places=2, currency='MYR')

    def get_total_price_for_checkout(self):  # including delivery cost
        if self.discount and self.discount.code == 'kota50460buku':
            amount = Money('1.00', 'MYR')
        else:
            amount = self.get_total_book_price_with_discount() + self.get_delivery_cost()
        return amount

    def get_total_price_in_toyyibpay_format(self):
        amount = self.get_total_price_for_checkout()
        return amount.get_amount_in_sub_unit()  # will convert (for example) RM1.00 to 100 for toyyibpay


class CartItem(models.Model):
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE)
    item = models.ForeignKey(Book, on_delete=models.CASCADE)
    quantity = models.PositiveSmallIntegerField()
    added_on = models.DateTimeField(auto_now=True)

    def get_subtotal(self):
        return self.item.price * self.quantity

    def __str__(self):
        return f'{self.quantity} x {self.item.title}'
