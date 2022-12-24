from django.contrib import admin
from django.db.models import Count, Sum

from orders.models import Order, Tracking, OrderSummary


@admin.register(OrderSummary)
class OrderSummaryAdmin(admin.ModelAdmin):
    change_list_template = 'admin/order_summary_change_list.html'
    date_hierarchy = 'transaction_time'

    def changelist_view(self, request, extra_context=None):
        response = super().changelist_view(
            request,
            extra_context=extra_context
        )

        try:
            qs = response.context_data['c1'].queryset
        except (AttributeError, KeyError):
            return response

        metrics = {
            'total': Count('id'),
            'total_sales': Sum('amount')
        }

        response.context_data['summary'] = list(
            qs
                .values('order')
                .annotate(**metrics)
                .order_by('-total_sales')
        )

        return response


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    search_fields = 'bill_code',
    list_filter = 'status', 'user',
    list_display = 'user', 'cart_items', 'reference_number', 'status', 'reason', 'bill_code', 'amount', \
                   'transaction_time',

    def cart_items(self, obj):
        ret_str = ''
        for item in obj.cart.cartitem_set.all():
            ret_str += f'{item}\n'
        return ret_str

    class Meta:
        model = Order


@admin.register(Tracking)
class TrackingAdmin(admin.ModelAdmin):
    list_display = 'order', 'number', 'submitter', 'created_on'

    class Meta:
        model = Tracking
