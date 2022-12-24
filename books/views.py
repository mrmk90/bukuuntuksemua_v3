from django.views.generic.detail import DetailView
from django.views.generic.list import ListView

from dashboard.views import CartMixin
from .models import Book


class BookListView(ListView):
    queryset = Book.objects.prefetch_related('image_set').all()
    template_name = 'books/book-list.html'


class BookDetailView(CartMixin, DetailView):
    template_name = 'books/book-detail.html'

    def get_object(self, queryset=None):
        return Book.objects.prefetch_related('image_set').get(pk=self.kwargs['pk'])

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['books'] = Book.objects.prefetch_related('image_set').all()
        return context


class TerkiniView(CartMixin, ListView):
    queryset = Book.objects.terkini().prefetch_related('image_set')
    template_name = 'books/terkini.html'


class BestsellerView(CartMixin, ListView):
    queryset = Book.objects.bestseller().prefetch_related('image_set')
    template_name = 'books/bestseller.html'


class BookByPublisherView(CartMixin, BookListView):
    template_name = 'books/publisher.html'

    def get_queryset(self):
        queryset = Book.objects.filter(
            publisher__slug=self.kwargs['publisher']).prefetch_related(
            'image_set')
        return queryset


class BookByCategoryView(CartMixin, BookListView):
    template_name = 'books/category.html'

    def get_queryset(self):
        queryset = Book.objects.filter(category__slug=self.kwargs['category']).prefetch_related(
            'image_set')
        return queryset
