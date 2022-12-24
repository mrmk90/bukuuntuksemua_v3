from django.contrib import admin
from django.utils.html import format_html

from .models import Cart, CartItem, Discount, Delivery


@admin.register(Discount)
class DiscountAdmin(admin.ModelAdmin):
    list_display = 'id', 'code', 'discount', 'get_total_usage', 'status'

    def get_total_usage(self, instance):
        return instance.cart_set.filter(status=Cart.OLD).count()

    class Meta:
        model = Discount


class CartItemAdmin(admin.StackedInline):
    model = CartItem


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    search_fields = 'id', 'user',
    inlines = [CartItemAdmin]
    list_filter = 'status', 'user',
    list_display = 'id', 'get_cart_items_display', 'created_on', 'user', 'status', 'discount', 'get_delivery_display'

    def get_delivery_display(self, instance):
        delivery = instance.delivery
        if delivery:
            return format_html(f'{delivery.name}<br>{delivery.address}<br>{delivery.postcode}, {delivery.state}')
        else:
            return '-'

    def get_cart_items_display(self, instance):
        cart_items = f''
        for item in instance.cartitem_set.all():
            cart_items = cart_items + f'{item}<br>'
        return format_html(cart_items)

    class Meta:
        model = Cart


@admin.register(Delivery)
class DeliveryAdmin(admin.ModelAdmin):
    list_display = [f.name for f in Delivery._meta.fields]

    class Meta:
        model = Delivery
