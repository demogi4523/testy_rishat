import os
import socket

from django.core.management.base import BaseCommand, CommandError
import stripe
from dotenv import find_dotenv, load_dotenv


load_dotenv(find_dotenv())

stripe.api_key = os.environ["STRIPE_API_SECRET_KEY"]

class Command(BaseCommand):
    help = 'Just add Stripe webhook for Checkout Session handle complete and expire events'

    def add_arguments(self, parser):
        parser.add_argument('scheme', nargs='?', type=str, default='http')

    def handle(self, *args, **options):
        try:
            scheme = options.get('scheme', 'http')
            try:
                HOSTNAME = socket.gethostname()
            except:
                HOSTNAME = 'localhost'

            domain = scheme + '://' + HOSTNAME
            stripe.WebhookEndpoint.create(
                url=f"{domain}/webhook",
                enabled_events=[
                    "checkout.session.completed",
                    "checkout.session.expired",
                ],
            )

            self.stdout.write(self.style.SUCCESS('Successfully add Stripe webhook'))
        except CommandError:
            django_command_name = os.path.basename(__file__).replace('.py','')
            self.stdout.write(self.style.ERROR(f"Something wring with {django_command_name} django command"))
        except Exception as err:
            self.stdout.write(self.style.ERROR(f"Something wrong\n{err}"))