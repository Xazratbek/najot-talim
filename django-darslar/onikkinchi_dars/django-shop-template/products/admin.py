from django.contrib import admin
from .models import Product, ProductImage, Category, PromoCode, PromoCodeUsage

admin.site.register(Category)

class ProductImageInline(admin.TabularInline):
    model = ProductImage
    extra = 5

@admin.register(Product)
class ProductAdmin(admin.ModelAdmin):
    inlines = [ProductImageInline]
    list_display = ["id","category","price"]
    list_filter = ["category", 'discount']
    search_fields = ["title","desc"]
    pass


@admin.register(PromoCode)
class PromoCodeAdmin(admin.ModelAdmin):
    list_display = (
        'code',
        'discount_type',
        'discount_value',
        'min_order_amount',
        'is_active',
        'expire_at',
        'total_usages'
    )
    list_filter = ('is_active', 'discount_type', 'expire_at')
    search_fields = ('code',)
    list_editable = ('is_active',)

    def total_usages(self, obj):
        # Displays the sum of usage_count for this promocode
        from django.db.models import Sum
        total = obj.usages.aggregate(Sum('usage_count'))['usage_count__sum']
        return total if total else 0
    total_usages.short_description = "Total Times Used"

@admin.register(PromoCodeUsage)
class PromoCodeUsageAdmin(admin.ModelAdmin):
    list_display = ('user', 'promocode', 'usage_count', 'last_used_at')
    list_filter = ('promocode', 'last_used_at')
    search_fields = ('user__username', 'promocode__code')
    readonly_fields = ('last_used_at',)
