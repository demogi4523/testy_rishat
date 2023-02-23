import os

from django.core.management.base import BaseCommand, CommandError

from products.models import Item, Tax, Discount

items_fixture = [
    {
        "name": "T-Short",
        "description": "Beautiful T-Short for any life situation",
        "price": "200000",
        "remained": 25,
        "active": True,
        "tax": 13,
    },
    {
        "name": "Sweater",
        "description": "A warm sweater especially for the Siberian winter",
        "price": "250000",
        "remained": 8,
        "active": True,
        "tax": 13,
        "discount": 20,
    },
    {
        "name": "Sneakers Nike",
        "description": "Incomparable original nikes",
        "price": "400000",
        "remained": 12,
        "active": True,
        "tax": 16,
    },
    {
        "name": "T-Short",
        "description": "Usual T-Short",
        "price": "150000",
        "remained": 254,
        "active": True,
        "tax": 20,
        "discount": 20,
    },
    {
        "name": "Wristband",
        "description": "A fashion accessory for the evening",
        "price": "5000000",
        "remained": 3,
        "active": True,
        "tax": 13,
        "discount": 5,
    },
]

class Command(BaseCommand):
    help = 'Just create fixture for manual testing'

    def handle(self, *args, **options):
        try:
            items = []
            tax, discount = None, None
            taxes, discounts = [], []
            for item in items_fixture:
                if "discount" in item:
                    discount = item["discount"]  #= Discount(item=new_item, percent=item["discount"])
                    del item["discount"]
                if "tax" in item:
                    tax = item["tax"]  #= Tax(item=new_item, percent=item["tax"])
                    del item["discount"]

                new_item = Item(**item)
                if discount:
                    discounts.append((item, discount))
                else:
                    discounts.append(())
                
                if tax:
                    taxes.append((item, tax))
                else:
                    taxes.append(())

            
            Item.objects.bulk_create(items)


            Discount.objects.bulk_create(discounts)
            Tax.objects.bulk_create(taxes)
            
            self.stdout.write(self.style.SUCCESS('Successfully filled database'))
        except CommandError:
            django_command_name = os.path.basename(__file__).replace('.py','')
            self.stdout.write(self.style.ERROR(f"Something wring with {django_command_name} django command"))
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"Something wrong\n{err}"))