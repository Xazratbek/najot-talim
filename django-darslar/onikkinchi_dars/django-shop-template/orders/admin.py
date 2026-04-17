from django.contrib import admin
from .models import Card, CardItem, Order, OrderItem

class CardItemInline(admin.TabularInline):
    model = CardItem
    extra = 1
    readonly_fields = ('total_price',)

class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 0
    readonly_fields = ('total_price',)

@admin.register(Card)
class CardAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'created_at')
    search_fields = ('user__username', 'user__email')
    inlines = [CardItemInline]

@admin.register(CardItem)
class CardItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'card', 'product', 'quantity', 'total_price')
    list_filter = ('card__user',)
    readonly_fields = ('total_price',)

@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = ('id', 'user', 'status', 'finished_price_display', 'created_at')
    list_filter = ('status', 'created_at')
    search_fields = ('user__username', 'address')
    inlines = [OrderItemInline]
    list_editable = ('status',)

    def finished_price_display(self, obj):
        return f"${obj.finished_price}"
    finished_price_display.short_description = "Total Price"

@admin.register(OrderItem)
class OrderItemAdmin(admin.ModelAdmin):
    list_display = ('id', 'order', 'product', 'quantity', 'total_price')
    readonly_fields = ('total_price',)
