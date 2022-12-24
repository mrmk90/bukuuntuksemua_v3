from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import Book, Image, Publisher, Category


class BookImageAdmin(admin.StackedInline):
    model = Image


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = 'name', 'slug'

    class Meta:
        model = Category


@admin.register(Publisher)
class PublisherAdmin(admin.ModelAdmin):
    list_display = 'name', 'slug'

    class Meta:
        model = Publisher


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    inlines = [BookImageAdmin]
    list_display = 'title', 'author', 'price', 'year', 'publisher', 'in_stock'

    class Meta:
        model = Book


class CustomUserAdmin(UserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'date_joined')


admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)
