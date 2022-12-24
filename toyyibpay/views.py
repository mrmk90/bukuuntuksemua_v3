from django.http import HttpResponse
from django.views.decorators.csrf import csrf_exempt
from django.views.generic import TemplateView

from carts.models import Cart
from orders.models import Order


@csrf_exempt
def payment_callback(request):
    data = request.POST

    order = Order.objects.select_related('cart').prefetch_related('cart__cartitem_set').get(
        bill_code=data.get('billcode'))
    order.reference_number = data.get('refno')
    order.status = data.get('status')
    order.reason = data.get('reason')
    order.transaction_time = data.get('transaction_time')

    if data.get('status') in (1, '1'):  # Berjaya
        # change cart status and deduct all confirmed order from stocks
        order.cart.status = Cart.OLD
        order.cart.save()

        for cartitem in order.cart.cartitem_set.all():
            book = cartitem.item
            book.in_stock = book.in_stock - cartitem.quantity
            book.save()

    order.save()
    return HttpResponse(content=b'OK', status=200)


class PaymentResult(TemplateView):
    """
    Example:
    http://mart.boca.my/payment-result?status_id=1&billcode=bc8665j9&order_id=&msg=ok&transaction_id=TP10653401191113515280721
    """
    template_name = 'toyyibpay/payment-result.html'
