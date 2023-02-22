from django.db import models
from django.contrib.auth.models import User


class Item(models.Model):
    name = models.CharField(max_length=128)
    description = models.TextField(null=True)
    price = models.IntegerField(null=False, default=1_000_000)
    remained = models.PositiveSmallIntegerField(default=1)
    active = models.BooleanField(default=True)

    def serialize(self):
        return {
            "pk": self.pk,
            "name": self.name,
            "description": self.description,
            "price": self.price,
            "remained": self.remained,
            "active": self.active,
        }
    
    # TODO: make it!!!
    def reserve(self, amount):
        try:
            pass
        except Exception as err:
            pass

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
    items = models.ForeignKey(
        'CartItem', 
        on_delete=models.DO_NOTHING, 
        related_name='cart_items',
        null=True,
    )

    def __str__(self) -> str:
        return f"{self.user}'s cart"
    

    def get_custom_items(self):
        items = CartItem.objects.filter(cart=self.pk)
        return ", ".join((str(item) for item in items))
    

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


class Order(models.Model):
    pass


class Discount(models.Model):
    pass


class Tax(models.Model):
    pass
