from django.db import models


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
            # "price": self.price,
        }
    
    def __str__(self) -> str:
        return self.name
    