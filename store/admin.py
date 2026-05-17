"""
Store Admin - Full Django admin with inline image upload
"""
from django.contrib import admin
from django.utils.html import format_html
from .models import Category, Brand, Product, ProductImage, ProductVariant, Banner, Coupon


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 3
    fields = ['image', 'alt_text', 'is_primary', 'order', 'image_preview']
    readonly_fields = ['image_preview']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:80px;height:80px;object-fit:cover;border-radius:8px;">', obj.image.url)
        return "No image"
    image_preview.short_description = 'Preview'


class ProductVariantInline(admin.TabularInline):
    model = ProductVariant
    extra = 2


@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ['name', 'parent', 'product_count', 'is_active', 'order', 'image_preview']
    list_filter = ['is_active', 'parent']
    list_editable = ['is_active', 'order']
    prepopulated_fields = {'slug': ('name',)}
    search_fields = ['name']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:50px;height:50px;object-fit:cover;border-radius:8px;">', obj.image.url)
        return "—"
    image_preview.short_description = 'Image'


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ['name', 'is_active']
    list_editable = ['is_active']
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    list_display = [
        'image_preview', 'name', 'category', 'brand', 'price', 'current_price_display',
        'stock_quantity', 'stock_status', 'is_active', 'is_featured', 'is_trending',
        'is_new_arrival', 'average_rating_display'
    ]
    list_filter = ['category', 'brand', 'is_active', 'is_featured', 'is_trending', 'is_new_arrival', 'stock_status']
    list_editable = ['is_active', 'is_featured', 'is_trending', 'is_new_arrival', 'stock_quantity']
    search_fields = ['name', 'sku', 'description']
    prepopulated_fields = {'slug': ('name',)}
    inlines = [ProductImageInline, ProductVariantInline]
    readonly_fields = ['sku', 'created_at', 'updated_at', 'discount_percent', 'main_image_preview']
    fieldsets = (
        ('Basic Info', {
            'fields': ('name', 'slug', 'sku', 'category', 'brand', 'short_description', 'description')
        }),
        ('Pricing', {
            'fields': ('price', 'discount_price', 'discount_percent')
        }),
        ('Inventory', {
            'fields': ('stock_quantity', 'stock_status')
        }),
        ('Main Image', {
            'fields': ('image', 'main_image_preview')
        }),
        ('Flags', {
            'fields': ('is_active', 'is_featured', 'is_trending', 'is_new_arrival', 'is_best_seller')
        }),
        ('SEO', {
            'fields': ('meta_title', 'meta_description'),
            'classes': ('collapse',)
        }),
        ('Specs', {
            'fields': ('specifications',),
            'classes': ('collapse',)
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at'),
            'classes': ('collapse',)
        }),
    )

    def image_preview(self, obj):
        img = obj.main_image
        if img:
            return format_html('<img src="{}" style="width:60px;height:60px;object-fit:cover;border-radius:8px;">', img.url)
        return "—"
    image_preview.short_description = 'Image'

    def main_image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="max-width:200px;border-radius:12px;">', obj.image.url)
        return "No image uploaded"
    main_image_preview.short_description = 'Preview'

    def current_price_display(self, obj):
        if obj.discount_price:
            return format_html('<span style="color:#ef4444;font-weight:bold;">${}</span>', obj.discount_price)
        return f'${obj.price}'
    current_price_display.short_description = 'Sale Price'

    def average_rating_display(self, obj):
        rating = obj.average_rating
        stars = '★' * int(rating) + '☆' * (5 - int(rating))
        return format_html('<span style="color:#f59e0b;">{}</span> ({})', stars, rating)
    average_rating_display.short_description = 'Rating'


@admin.register(Banner)
class BannerAdmin(admin.ModelAdmin):
    list_display = ['title', 'is_active', 'order', 'image_preview']
    list_editable = ['is_active', 'order']

    def image_preview(self, obj):
        if obj.image:
            return format_html('<img src="{}" style="width:120px;height:60px;object-fit:cover;border-radius:8px;">', obj.image.url)
        return "—"
    image_preview.short_description = 'Preview'


@admin.register(Coupon)
class CouponAdmin(admin.ModelAdmin):
    list_display = ['code', 'discount_type', 'discount_value', 'is_active', 'valid_from', 'valid_to', 'used_count']
    list_editable = ['is_active']
    list_filter = ['discount_type', 'is_active']
