from __future__ import annotations
from typing import Iterable, List

from django.db import models
# from django.core.validators import MaxValueValidator, MinValueValidator
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    price = models.IntegerField(null=False, default=100_000_000)
    remained = models.PositiveSmallIntegerField(default=1)
    active = models.BooleanField(default=True)

    # tax = models.OneToOneField(
    #     'Tax', 
    #     on_delete=models.CASCADE, 
    #     related_name='item_tax', 
    #     blank=True,
    #     null=True, 
    # )
    # discount = models.OneToOneField(
    #     'Discount', 
    #     on_delete=models.CASCADE, 
    #     related_name='item_discount', 
    #     blank=True,
    #     null=True, 
    # )

    def serialize(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "remained": self.remained,
            "active": self.active,
        }
    
    def reserve(self, amount):
        try:
            self.remained -= amount
            self.save()
        except Exception as err:
            raise Exception(f"Something wrong in Item.reserve:\n{err}")

    def get_data(self):
        return {
            "name": self.name,
            "description": self.description,
        }
    
    def __str__(self) -> str:
        return self.name
    

class ItemImage(models.Model):
    pass


class Cart(models.Model):
    user = models.OneToOneField(
        User,
        on_delete=models.CASCADE,
        unique=True,
        primary_key=True,
    )

    def __str__(self) -> str:
        return f"{self.user}'s cart"
    

    def add_item(self, item: Item, quantity: int):
        cart_item = CartItem(item=item, cart=self, quantity=quantity)
        cart_item.save()


    def get_custom_items(self):
        items = CartItem.objects.filter(cart=self.pk)
        return ", ".join((str(item) for item in items))
    
    def get_items(self):
        return CartItem.objects.filter(cart=self.pk)
    
    def summarize(self):
        total = 0
        items = self.get_items()
        for item in items:
            val = item.item.price
            # if item.item.discount:
            #     val *= (1 - item.item.discount / 100)
            total += val * item.quantity
        return total
    
    def clear(self):
        current_cart = Cart.objects.get(pk=self.pk)
        current_cart_items = CartItem.objects.filter(cart=current_cart)
        current_cart_items.delete()

    @classmethod
    def get_cart_by_user(_, user: User) -> Cart:
        return Cart.objects.get(user=user)


class CartItem(models.Model):
    id = models.BigAutoField(primary_key=True)
    cart = models.ForeignKey(
        Cart,
        on_delete=models.CASCADE,
    )
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self) -> str:
        return f"{self.cart}: {self.item}"


class OrderItem(models.Model):
    from_order = models.ForeignKey("Order", on_delete=models.CASCADE)
    item = models.ForeignKey(Item, on_delete=models.DO_NOTHING)
    quantity = models.PositiveSmallIntegerField(default=1)

    def __str__(self) -> str:
        return f"{str(self.item)} x {self.quantity}"


class Order(models.Model):
    id = models.BigAutoField(primary_key=True)
    user = models.ForeignKey(
        User,
        on_delete=models.DO_NOTHING,
        null=True,
    )
    payed = models.BooleanField(default=False)
    stripe_checkout_session_id = models.CharField(max_length=256, null=True, blank=True)

    def __str__(self) -> str:
        return f"From: {self.user} #{self.pk}"

    def get_items(self):
        return OrderItem.objects.filter(from_order=self.pk)

    @classmethod
    def reserve(_, cart: Cart):
        items = cart.get_items()
        for item in items:
            item.item.reserve(item.quantity)


    @classmethod
    def create_from_cart(_, cart: Cart, payed: bool = False) -> Order:
        new_order = Order()
        new_order.save()
        
        items = []
        for item in cart.get_items():
            new_order_item = OrderItem(
                from_order=new_order,
                item=item.item,
                quantity=item.quantity,
            )
            items.append(new_order_item)
        OrderItem.objects.bulk_create(items)

        new_order.user=cart.user
        new_order.payed=payed

        new_order.save()
        return new_order

    @classmethod
    def check_items_availability(_, items: Iterable[CartItem], bad_items: List = []) -> bool:
        for item in items:
            if item.quantity > item.item.remained:
                bad_items.append((
                    item, 
                    f"Order quantity: {item.quantity}", 
                    f"In stock remained: {item.item.remained}",
                ))

        if len(bad_items) == 0:
            return True
        return False

    def check_order_items_availability(self, bad_items: List = []) -> bool:
        return Order.check_items_availability(self.items, bad_items)

    def mark_payed(self):
        self.payed = True
        self.save()


    def summarize(self):
        total = 0
        items = self.get_items()

        for item in items:
            val = item.item.price
            # if item.item.discount:
            #     val *= (1 - item.item.discount / 100)
            total += val * item.quantity
        return total

# class Discount(models.Model):
#     item = models.OneToOneField(
#         Item, 
#         on_delete=models.CASCADE, 
#         related_name='dicount_item',
#         null=True,
#     )
#     percent = models.IntegerField(
#         default=1,
#         validators=[
#             MaxValueValidator(99),
#             MinValueValidator(1),
#         ]
#     )

#     def __str__(self) -> str:
#         return f"{self.item}'s with {self.percent} discount and {self.item.pk} id"


# class Tax(models.Model):
#     item = models.OneToOneField(
#         Item, 
#         on_delete=models.CASCADE,
#         related_name='tax_item',
#         null=True,
#     )
#     percent = models.IntegerField(
#         default=10,
#         validators=[
#             MaxValueValidator(99),
#             MinValueValidator(1),
#         ]
#     )

#     class Meta:
#         verbose_name_plural = 'Taxes'

#     def __str__(self) -> str:
#         return f"{self.item}'s with id {self.item.pk} tax"
