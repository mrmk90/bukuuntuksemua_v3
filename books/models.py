import datetime

from django.core.validators import MaxValueValidator, MinValueValidator
from django.db import models
from django.db.models import Sum
from django.urls import reverse
from django_extensions.db.fields import AutoSlugField
from djmoney.models.fields import MoneyField


class Publisher(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', max_length=50)

    def __str__(self):
        return self.name


class Category(models.Model):
    name = models.CharField(max_length=100)
    slug = AutoSlugField(populate_from='name', max_length=50)

    def __str__(self):
        return self.name


class BookManager(models.Manager):
    def terkini(self):
        return self.order_by('-id')

    def bestseller(self):
        return self.filter(cartitem__cart__order__status__in=(1, 4)).annotate(
            total_sold=Sum('cartitem__quantity')).order_by('-total_sold')


class Book(models.Model):
    title = models.CharField(max_length=250)
    author = models.CharField(max_length=250)
    isbn = models.CharField(max_length=25)
    price = MoneyField(max_digits=14, decimal_places=2, default_currency='MYR')
    publisher = models.ForeignKey(Publisher, on_delete=models.SET_NULL, null=True)
    year = models.PositiveIntegerField(
        default=datetime.date.today().year,
        validators=[MinValueValidator(1900), MaxValueValidator(datetime.date.today().year)]
    )
    synopsis = models.TextField(default='')
    pages = models.PositiveIntegerField()
    category = models.ManyToManyField(Category)
    in_stock = models.PositiveIntegerField()
    objects = BookManager()

    def __str__(self):
        return self.title + ' by ' + self.author

    def get_book_url(self):
        return reverse('book-detail', args=self.id)


class Image(models.Model):
    book = models.ForeignKey(Book, default=None, on_delete=models.CASCADE)
    images = models.FileField()
