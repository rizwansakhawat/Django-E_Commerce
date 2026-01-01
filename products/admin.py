from django.contrib import admin
from .models import (
    Category, Brand, Product, ProductImage,
    ProductReview, ProductSpecification, ProductDescription, ProductAdditionalInfo
)

# Register your models here.

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


@admin.register(Brand)
class BrandAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}


class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 1
    fields = ('image', 'alt_text')


class ProductSpecificationInline(admin.TabularInline):
    model = ProductSpecification
    extra = 1


class ProductDescriptionInline(admin.StackedInline):
    model = ProductDescription
    extra = 1
    fields = ('title', 'content', 'image', 'order')


class ProductAdditionalInfoInline(admin.TabularInline):
    model = ProductAdditionalInfo
    extra = 1
    fields = ('attribute_name', 'attribute_value', 'order')


@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline, ProductSpecificationInline, ProductDescriptionInline, ProductAdditionalInfoInline]
    list_display = ('name', 'category', 'brand', 'price', 'discount_price', 'stock', 'is_available', 'is_featured', 'created_at')
    list_filter = ('category', 'brand', 'is_available', 'is_featured', 'is_promotion', 'created_at')
    search_fields = ('name', 'sku')
    prepopulated_fields = {'slug': ('name',)}
    readonly_fields = ('created_at', 'updated_at')
    
    fieldsets = (
        ('Basic Information', {
            'fields': ('name', 'slug', 'sku', 'category', 'brand')
        }),
        ('Product Details', {
            'fields': ('short_description', 'main_image')
        }),
        ('Pricing & Stock', {
            'fields': ('price', 'discount_price', 'stock', 'is_available')
        }),
        ('Features', {
            'fields': ('is_featured', 'is_promotion', 'promotion_theme', 'promotion_size')
        }),
        ('Warranty', {
            'fields': ('warranty_years', 'warranty_info')
        }),
        ('Timestamps', {
            'fields': ('created_at', 'updated_at')
        }),
    )


@admin.register(ProductImage)
class ProductImageAdmin(admin.ModelAdmin):
    list_display = ('product', 'alt_text', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'alt_text')


@admin.register(ProductReview)
class ProductReviewAdmin(admin.ModelAdmin):
    list_display = ('product', 'user', 'rating', 'title', 'is_approved', 'created_at')
    list_filter = ('rating', 'is_approved', 'created_at')
    search_fields = ('product__name', 'user__username', 'title', 'comment')
    readonly_fields = ('created_at', 'updated_at')
    actions = ['approve_reviews', 'disapprove_reviews']
    
    def approve_reviews(self, request, queryset):
        queryset.update(is_approved=True)
    approve_reviews.short_description = "Approve selected reviews"
    
    def disapprove_reviews(self, request, queryset):
        queryset.update(is_approved=False)
    disapprove_reviews.short_description = "Disapprove selected reviews"


@admin.register(ProductSpecification)
class ProductSpecificationAdmin(admin.ModelAdmin):
    list_display = ('product', 'specification')
    search_fields = ('product__name', 'specification')


@admin.register(ProductDescription)
class ProductDescriptionAdmin(admin.ModelAdmin):
    list_display = ('product', 'title', 'order', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('product__name', 'title', 'content')
    ordering = ('product', 'order')


@admin.register(ProductAdditionalInfo)
class ProductAdditionalInfoAdmin(admin.ModelAdmin):
    list_display = ('product', 'attribute_name', 'order')
    search_fields = ('product__name', 'attribute_name')
    ordering = ('product', 'order')
