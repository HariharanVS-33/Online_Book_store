from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Book, Subscriber, Cart, CartItem, Order, OrderItem, UserProfile


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'icon', 'slug', 'book_count', 'created_at')
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ('name',)

    def book_count(self, obj):
        return obj.books.count()
    book_count.short_description = 'Books'


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('book', 'quantity', 'price', 'subtotal')

    def subtotal(self, obj):
        return f"₹{obj.subtotal}"


@admin.register(Book)
class BookAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'category', 'price', 'rating', 'stock',
                    'is_bestseller', 'is_new_arrival', 'cover_preview')
    list_filter = ('category', 'is_bestseller', 'is_new_arrival', 'is_audiobook', 'language')
    search_fields = ('title', 'author', 'isbn')
    list_editable = ('price', 'stock', 'is_bestseller', 'is_new_arrival')
    list_per_page = 20
    fieldsets = (
        ('Book Info', {'fields': ('title', 'author', 'isbn', 'description', 'cover_image')}),
        ('Category & Classification', {'fields': ('category', 'language', 'pages', 'published_year')}),
        ('Pricing & Stock', {'fields': ('price', 'stock', 'rating')}),
        ('Featured', {'fields': ('is_bestseller', 'is_new_arrival', 'is_audiobook')}),
    )

    def cover_preview(self, obj):
        if obj.cover_image:
            return format_html('<img src="{}" width="40" height="55" style="object-fit:cover; border-radius:4px;">', obj.cover_image.url)
        return '—'
    cover_preview.short_description = 'Cover'


@admin.register(Subscriber)
class SubscriberAdmin(admin.ModelAdmin):
    list_display = ('email', 'subscribed_at')
    search_fields = ('email',)
    readonly_fields = ('subscribed_at',)


class CartItemInline(admin.TabularInline):
    model = CartItem
    extra = 0


@admin.register(Cart)
class CartAdmin(admin.ModelAdmin):
    list_display = ('user', 'item_count', 'total', 'updated_at')
    inlines = [CartItemInline]
    readonly_fields = ('created_at', 'updated_at')

    def item_count(self, obj):
        return obj.item_count

    def total(self, obj):
        return f"₹{obj.total}"


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'full_name', 'total', 'status', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'full_name', 'email')
    list_editable = ('status',)
    inlines = [OrderItemInline]
    readonly_fields = ('created_at',)


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'phone', 'address')
    search_fields = ('user__username', 'user__email')
