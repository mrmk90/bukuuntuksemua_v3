import csv
import datetime

from django.contrib.auth.mixins import PermissionRequiredMixin
from django.contrib.auth.models import User
from django.db.models import Count, Sum, Q
from django.http import HttpResponse
from django.views.generic import TemplateView
from django.views.generic.base import ContextMixin

from books.models import Book
from carts.models import Cart, CartItem
from orders.models import Order


class CartMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)

        if self.request.user.is_authenticated:
            Cart.objects.get_or_create(status=Cart.NEW, user=self.request.user)
            cart = self.request.user.cart_set.prefetch_related('cartitem_set', 'cartitem_set__item',
                                                               'cartitem_set__item__image_set').get(status=Cart.NEW)
            context['cart'] = cart

        return context


def generate_csv_report(request):
    date_from = request.GET.get('from', None)
    date_to = request.GET.get('to', None)
    status_filter = request.GET.get('filter', None)

    if date_from and date_to and status_filter:
        filename = f'Report From {date_from} To - {datetime.datetime.now()}'
    elif date_from and date_to:
        filename = f'Full Report From {date_from} To {date_to} - {datetime.datetime.now()}'
    else:
        filename = f'All Time Report - {datetime.datetime.now()}'
    response = HttpResponse(
        content_type='text/csv',
        headers={'Content-Disposition': f'attachment; filename="{filename}.csv"'},
    )

    writer = csv.writer(response)
    writer.writerow(['ID', 'Username', 'Tajuk & Kuantiti', 'Rujukan', 'Tarikh', 'Kod Diskaun', 'Jumlah Asal',
                     'Jumlah Diskaun', 'Postage', 'Total Payment', 'Status'])

    if date_from and date_to and status_filter:
        order_data = Order.objects.filter(status=status_filter, transaction_time__date__range=[date_from, date_to]) \
            .select_related('user', 'cart__discount', 'cart__delivery') \
            .prefetch_related('cart__cartitem_set', 'cart__cartitem_set__item')

    elif date_from and date_to:
        order_data = Order.objects.filter(transaction_time__date__range=[date_from, date_to]) \
            .select_related('user', 'cart__discount', 'cart__delivery') \
            .prefetch_related('cart__cartitem_set', 'cart__cartitem_set__item')
    else:
        order_data = Order.objects.all().select_related('user', 'cart__discount', 'cart__delivery').prefetch_related(
            'cart__cartitem_set', 'cart__cartitem_set__item')

    for o in order_data:
        tajuk_kuantiti = ''
        for i in o.cart.cartitem_set.all():
            tajuk_kuantiti += f'{i.quantity} x {i.item}\n'

        discount_code = ''
        if o.cart.discount:
            discount_code = o.cart.discount.code

        writer.writerow([
            o.id, f'{o.user.username}\n{o.cart.delivery.name}', tajuk_kuantiti, o.get_billcode_url(),
            o.transaction_time, discount_code, o.cart.get_total_book_price(), o.cart.get_discount_amount(),
            o.cart.get_delivery_cost(), f'RM{o.display_amount():.2f}', o.get_status_display()
        ])
    return response


class ReportView(CartMixin, TemplateView):
    template_name = 'dashboard/report.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        date_from = self.request.GET.get('from', None)
        date_to = self.request.GET.get('to', None)
        status_filter = self.request.GET.get('filter', None)
        if date_from and date_to and status_filter:
            context['orders'] = Order.objects \
                .filter(status=status_filter, transaction_time__date__range=[date_from, date_to]) \
                .select_related('user', 'cart__discount', 'cart__delivery') \
                .prefetch_related('cart__cartitem_set', 'cart__cartitem_set__item')
        elif date_from and date_to:
            context['orders'] = Order.objects \
                .filter(transaction_time__date__range=[date_from, date_to]) \
                .select_related('user', 'cart__discount', 'cart__delivery') \
                .prefetch_related('cart__cartitem_set', 'cart__cartitem_set__item')
        else:
            context['orders'] = Order.objects.all().select_related('user', 'cart__discount',
                                                                   'cart__delivery').prefetch_related(
                'cart__cartitem_set', 'cart__cartitem_set__item')
        return context


class StatisticsView(PermissionRequiredMixin, CartMixin, TemplateView):
    template_name = 'dashboard/statistics.html'
    permission_required = ()

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['total_coupon_redeemed'] = Order.objects.all().aggregate(total_coupon_redeemed=Count('cart__discount'))[
            'total_coupon_redeemed']
        context['total_successful_coupon_redeemed'] = Order.objects.filter(status__in=(1, 4)).aggregate(
            total_successful_coupon_redeemed=Count('cart__discount'))['total_successful_coupon_redeemed']
        context['total_sales_amount'] = Order.objects.filter(status__in=(1, 4)).aggregate(Sum('amount'))[
                                            'amount__sum'] / 100
        context['total_books_sold'] = \
            CartItem.objects.filter(cart__order__status__in=(1, 4)).aggregate(Sum('quantity'))[
                'quantity__sum']
        context['users_with_multiple_coupon'] = User.objects.annotate(
            baucar_count=Count('cart', filter=Q(cart__discount__code='BaucarBOCA'))).order_by('-baucar_count')
        context['bestsellers'] = Book.objects.bestseller()
        return context


class IndexView(CartMixin, TemplateView):
    template_name = 'dashboard/index.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.prefetch_related('image_set').all()
        context['latest_books'] = Book.objects.terkini().prefetch_related('image_set')
        context['bestsellers'] = Book.objects.bestseller().prefetch_related('image_set')
        return context


class StatsView(TemplateView):
    template_name = 'dashboard/stats.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        books = Book.objects.all()
        context['books'] = books
        context['tajuk_buku'] = books.count()
        context['order_diproses'] = Order.objects.count()
        context['pelanggan_berdaftar'] = User.objects.count()
        return context


class TermaView(CartMixin, TemplateView):
    template_name = 'dashboard/terma.html'


class BaseView(CartMixin, TemplateView):
    template_name = 'base/base.html'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.all()

        return context


class PendaftaranView(CartMixin, TemplateView):
    template_name = 'dashboard/pendaftaran.html'
