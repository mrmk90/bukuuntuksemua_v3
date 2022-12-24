from django.contrib.admin.views.decorators import staff_member_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.core.paginator import Paginator
from django.shortcuts import redirect, render
from django.views.generic import TemplateView, ListView, CreateView

from carts.models import Delivery, Cart
from dashboard.views import CartMixin
from orders.models import Order, Tracking
from toyyibpay.api import ToyyibPay


class CreateTrackingView(CartMixin, CreateView):
    model = Tracking
    fields = 'number',
    success_url = '/process-order/'

    def form_valid(self, form):
        order = Order.objects.get(pk=self.kwargs['order_id'])
        order.status = 4
        order.save()
        form.instance.order = order
        form.instance.submitter = self.request.user
        return super().form_valid(form)


class OrderView(LoginRequiredMixin, CartMixin, ListView):
    template_name = 'orders/order-list.html'

    def get_queryset(self):
        user = self.request.user
        orders = Order.objects.prefetch_related('cart__cartitem_set', 'cart__cartitem_set__item').filter(user=user)
        return orders


class CheckoutView(CartMixin, TemplateView):
    template_name = 'orders/checkout.html'


def final_confirmation(request):
    cart = request.user.cart_set.prefetch_related('cartitem_set', 'cartitem_set__item').select_related('delivery').get(
        status=Cart.NEW)
    if cart.delivery:
        cart.delivery.name = request.POST['receiver_name']
        cart.delivery.address = request.POST['address']
        cart.delivery.postcode = request.POST['postcode']
        cart.delivery.state = request.POST['negeri']
        cart.delivery.phone_number = request.POST['phone']
        cart.delivery.save()
    else:
        cart.delivery = Delivery.objects.create(
            name=request.POST['receiver_name'],
            address=request.POST['address'],
            postcode=request.POST['postcode'],
            state=request.POST['negeri'],
            phone_number=request.POST['phone'],
        )
    cart.save()

    return render(
        request,
        'carts/final-confirmation.html',
        context={
            'cart': cart,
        }
    )


def create_order(request):
    cart = request.user.cart_set.prefetch_related('cartitem_set', 'cartitem_set__item').get(status=Cart.NEW)
    tpay = ToyyibPay()

    '''
    populate data to send to toyyibpay
    Rujukan: https://toyyibpay.com/apireference/
    '''
    data = {
        'billName': 'Pembelian Dari Boca Mart',
        'billDescription': 'Pembelian Buku Dari Boca Mart',
        'billPriceSetting': 1,  # 0 - user can set amount,  1 - fixed amount,
        'billPayorInfo': 1,
        'billAmount': cart.get_total_price_in_toyyibpay_format(),
        # 'billExternalReferenceNo': 'AFR341DFI', KIV
        'billTo': cart.delivery.name,
        'billEmail': request.user.email,
        'billPhone': cart.delivery.phone_number,
        'billPaymentChannel': '0',  # Set 0 for FPX, 1 Credit Card and 2 for both FPX & Credit Card
        'billContentEmail': 'Terima kasih atas pembelian anda di Boca Mart!',
        'billChargeToCustomer': 1
    }
    bill_code = tpay.create_bill(data=data)
    order = Order.objects.get_or_create(
        user=request.user,
        cart=cart,
    )[0]
    order.bill_code = bill_code['BillCode']
    order.amount = cart.get_total_price_in_toyyibpay_format()
    order.save()
    bill_url = 'https://toyyibpay.com/' + bill_code['BillCode']
    return redirect(to=bill_url)


@staff_member_required
def process_order(request):
    status = request.GET.get('status', None)
    status_code = {
        'Berjaya': 1,
        'Dalam Proses': 2,
        'Gagal': 3,
        'Sudah Dipos': 4,
    }
    if status:
        orders = Order.objects.filter(status=status_code[status]).select_related('tracking').prefetch_related(
            'cart__cartitem_set',
            'cart__delivery',
            'cart__cartitem_set__item').order_by('transaction_time')
    else:
        orders = Order.objects.all().select_related('tracking').prefetch_related('cart__cartitem_set', 'cart__delivery',
                                                                                 'cart__cartitem_set__item').order_by(
            'transaction_time')

    # paginator = Paginator(orders, 10)
    # page_number = request.GET.get('page')
    # page_obj = paginator.get_page(page_number)

    return render(
        request,
        'orders/process-order.html',
        context={
            # 'page_obj': page_obj,
            'orders': orders,
        }
    )
