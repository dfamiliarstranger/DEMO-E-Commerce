from django.contrib import admin
from store.models import  Category, Tax, Product, Gallery, Specification, Color, Size, Cart, CartOrder, CartOrderItem, ProductFaq, Review,Wishlist, Notification, Coupon

class SpecificationInline(admin.TabularInline):
    model = Specification
    extra = 0

class ColorInline(admin.TabularInline):
    model = Color
    extra = 0

class SizeInline(admin.TabularInline):
    model = Size
    extra = 0

class GalleryInline(admin.TabularInline):
    model = Gallery
    extra = 0

class ProductAdmin(admin.ModelAdmin):
    list_display = ['title', 'price','category', 'featured', 'shipping_amount', 'stock_qty', 'in_stock', 'vendor']
    inlines=[GalleryInline, SpecificationInline, ColorInline, SizeInline]

class CartAdmin(admin.ModelAdmin):
    list_display = ['product', 'cart_id', 'qty', 'price', 'sub_total' , 'shipping_amount', 'service_fee', 'tax_fee', 'total', 'country', 'size', 'color', 'date']

# admin.site.register(Product, ProductAdmin)
admin.site.register(Category)
admin.site.register(Product, ProductAdmin)
admin.site.register(Cart, CartAdmin)
admin.site.register(CartOrder)
admin.site.register(CartOrderItem)
admin.site.register(ProductFaq)
admin.site.register(Review)
admin.site.register(Wishlist)
admin.site.register(Notification)
admin.site.register(Coupon)
admin.site.register(Tax)
