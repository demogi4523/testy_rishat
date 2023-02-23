from django.contrib import admin

from products.models import (
    Item, 
    Cart, CartItem, 
    Order, OrderItem,
)

@admin.register(OrderItem)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'from_order', 
        'item',
        'quantity',
    )


@admin.register(Order)
class OrderAdmin(admin.ModelAdmin):
    list_display = (
        'user', 
        'get_items',
    )
    fieldsets = (
      ('Order info', {
          'fields': ('user', 'payed', 'get_items')
      }),
    )
    readonly_fields = ('get_items', )

    @admin.display(description='Order Items')
    def get_items(self, obj):
        orders = OrderItem.objects.filter(from_order=obj.pk)
        return ", ".join((f"{str(order.item)} x {order.quantity}" for order in orders))



@admin.register(Item)
class AdminItem(admin.ModelAdmin):
    list_display = (
        'name',
        'remained',
    )


admin.site.register(CartItem)


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = (
        'user', 
        'get_items',
    )
    fieldsets = (
      ('Standard info', {
          'fields': ('user',)
      }),
    )
    
    @admin.display(description='CC Items')
    def get_items(self, obj):
        items = CartItem.objects.filter(cart=obj.pk)
        return ", ".join((f"{str(item.item)} x {str(item.quantity)}" for item in items))
