from django.contrib.auth.decorators import login_required
from django.shortcuts import redirect
from django.urls import reverse
from django.views.generic import TemplateView, UpdateView
from django.views.generic.base import ContextMixin

from books.models import Book
from .models import Cart, CartItem, Discount


class CartMixin(ContextMixin):
    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['cart'] = \
            Cart.objects.prefetch_related('cartitem_set', 'cartitem_set__item',
                                          'cartitem_set__item__image_set').get_or_create(user=self.request.user,
                                                                                         status=Cart.NEW)[0]
        return context


class CartView(CartMixin, TemplateView):
    template_name = 'carts/cart-view.html'


class DiscountCodeErrorView(CartMixin, TemplateView):
    template_name = 'carts/code-not-found.html'


class DiscountCodeRedeemedView(DiscountCodeErrorView):
    template_name = 'carts/code-redeemed.html'


class DiscountCodeExpiredView(DiscountCodeErrorView):
    template_name = 'carts/code-expired.html'


@login_required
def add_discount(request):
    discount_code = request.POST.get('coupon_code')
    cart = Cart.objects.get(user=request.user, status=Cart.NEW)

    try:
        discount = Discount.objects.get(code=discount_code)

        # Check for discount status
        if discount.status == Discount.EXPIRED:
            return redirect(reverse('discount-code-expired'))

        # Check for multiple discount code usage (limit current == 1)
        if Cart.objects.filter(user=request.user, discount=discount).count() > 0:
            return redirect(reverse('discount-code-redeemed'))

        cart.discount = discount
        cart.save()
        return redirect(reverse('cart-detail'))
    except Discount.DoesNotExist:
        return redirect(reverse('discount-code-error'))


@login_required
def add_to_cart(request, book_id):
    cart = Cart.objects.get(user=request.user, status=Cart.NEW)
    book = Book.objects.get(id=book_id)

    # check if the book already exist in cart
    if CartItem.objects.filter(item=book, cart=cart).exists():
        cart_item = CartItem.objects.get(cart=cart, item=book)
        cart_item.quantity += 1
        cart_item.save()
    else:
        CartItem(cart=cart, item=book, quantity=1).save()

    return redirect(request.GET.get('next', '/'))


@login_required
def delete_from_cart(request, cartitem_id):
    # to ensure that user can only delete cartitem in their own cart
    cart = Cart.objects.prefetch_related('cartitem_set').get(user=request.user, status=Cart.NEW)
    cartitem = cart.cartitem_set.get(pk=cartitem_id)
    cartitem.delete()

    return redirect(request.GET.get('next', '/'))


class UpdateStateView(CartMixin, UpdateView):
    template_name = 'carts/update-state.html'

    def get_queryset(self):
        return Cart.objects.get(user=self.request.user, status=Cart.NEW)
