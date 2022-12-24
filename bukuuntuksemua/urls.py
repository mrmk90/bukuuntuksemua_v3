"""bukuuntuksemua URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
import debug_toolbar
from django.conf import settings
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import include, path

from books.views import BookDetailView, BookListView, TerkiniView, BestsellerView, BookByCategoryView, \
    BookByPublisherView
from carts.views import CartView, add_to_cart, delete_from_cart, add_discount, DiscountCodeErrorView, UpdateStateView, \
    DiscountCodeRedeemedView, DiscountCodeExpiredView
from dashboard.views import IndexView, StatsView, BaseView, TermaView, PendaftaranView, StatisticsView, ReportView, \
    generate_csv_report
from orders.views import OrderView, CheckoutView, create_order, final_confirmation, process_order, CreateTrackingView
from toyyibpay.views import PaymentResult, payment_callback

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', IndexView.as_view(), name='index'),
    path('statistics', StatisticsView.as_view(), name='statistics'),
    path('report', ReportView.as_view(), name='report'),
    path('generate-csv-report', generate_csv_report, name='generate-csv-report'),
    path('stats', StatsView.as_view(), name='stats'),
    path('base', BaseView.as_view(), name='base'),
    path('terma', TermaView.as_view(), name='terma'),
    path('pendaftaran', PendaftaranView.as_view(), name='pendaftaran'),

    # books
    path('terkini', TerkiniView.as_view(), name='terkini'),
    path('bestseller', BestsellerView.as_view(), name='bestseller'),
    path('category/<str:category>', BookByCategoryView.as_view(), name='book-by-category'),
    path('publisher/<str:publisher>', BookByPublisherView.as_view(), name='book-by-publisher'),
    path('books/', BookListView.as_view(), name='book-list'),
    path('books/<int:pk>', BookDetailView.as_view(), name='book-detail'),

    # carts
    path('cart/', CartView.as_view(), name='cart-detail'),
    path('cart/add/<int:book_id>', add_to_cart, name='add-to-cart'),
    # path('cart/update'),
    # path('cart/add'),
    path('cart/delete/<int:cartitem_id>', delete_from_cart, name='delete-from-cart'),
    path('add-discount/', add_discount, name='add-discount'),
    path('discount-code-error', DiscountCodeErrorView.as_view(), name='discount-code-error'),
    path('discount-code-redeem', DiscountCodeRedeemedView.as_view(), name='discount-code-redeemed'),
    path('discount-code-expired', DiscountCodeExpiredView.as_view(), name='discount-code-expired'),
    path('update-state', UpdateStateView.as_view(), name='update-state'),

    # orders
    path('orders/', OrderView.as_view(), name='orders'),
    path('checkout/', CheckoutView.as_view(), name='checkout'),
    path('final-confirmation/', final_confirmation, name='final-confirmation'),
    path('create-order/', create_order, name='create-order'),
    path('process-order/', process_order, name='process-order'),
    path('create-tracking/<int:order_id>', CreateTrackingView.as_view(), name='create-tracking'),

    # toyyibpay
    path('payment-result', PaymentResult.as_view(), name='payment-result'),
    path('payment-callback', payment_callback, name='payment-callback'),

    # django-registration
    path('accounts/', include('django_registration.backends.one_step.urls')),
    path('accounts/', include('django.contrib.auth.urls')),

    # helper urls
    path('hijack/', include('hijack.urls')),
    path('__debug__/', include(debug_toolbar.urls)),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)