from django.contrib import admin
from order.models import Order, OrderItem

# Register your models here.


class OrderItemInline(admin.TabularInline):
    model = OrderItem
    extra = 1


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = 'id', 'user', 'total', 'status'
    list_display_links = 'id',
    search_fields = 'id', 'user', 'total', 'status'
    list_per_page = 10
    ordering = '-id',
    inlines = OrderItemInline,
