import os

from django.core.management.base import BaseCommand, CommandError

from products.models import Item

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
            items = [Item(**item) for item in items_fixture]
            Item.objects.bulk_create(items)
            self.stdout.write(self.style.SUCCESS('Successfully filled database'))
        except CommandError:
            django_command_name = os.path.basename(__file__).replace('.py','')
            self.stdout.write(self.style.ERROR(f"Something wring with {django_command_name} django command"))
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"Something wrong\n{err}"))