from django.db import models
from django.contrib import admin
from django import forms
from django.contrib.admin import widgets

from products.models import Item, Cart, CartItem


admin.site.register(Item)
admin.site.register(CartItem)


class CartAdminForm(forms.ModelForm):
    items = forms.SelectMultiple(choices=('A', 'B', 'C'))


@admin.register(Cart)
class AdminCart(admin.ModelAdmin):
    list_display = (
        'user', 
        'get_items',
    )
    fieldsets = (
      ('Standard info', {
          'fields': ('user', 'items')
      }),
    )
    
    @admin.display(description='CC Items')
    def get_items(self, obj):
        items = CartItem.objects.filter(cart=obj.pk)
        return ", ".join((str(item.item) for item in items))