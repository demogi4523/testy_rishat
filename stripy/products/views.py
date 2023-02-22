import os

from django.http import HttpRequest, HttpResponseBadRequest
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.generic.base import TemplateView
from django.http.response import JsonResponse
from django.views.decorators import http
from django.shortcuts import render
import stripe
from dotenv import load_dotenv, find_dotenv

from products.models import Item, Cart


class ItemListView(ListView):
    model = Item
    context_object_name = "items"


class ItemView(DetailView):
    model = Item


load_dotenv(find_dotenv())
stripe.api_key = os.environ['STRIPE_API_SECRET_KEY']

def get_pk(_):
    pk_key = os.environ['STRIPE_API_PUBLIC_KEY']
    return JsonResponse({
        "pk": pk_key,
    })

@http.require_GET
def create_checkout_session(request: HttpRequest, pk):
    try:
        product = Item.objects.get(pk=pk)

        amount = int(request.GET['amount'])
        
        domain = request.scheme + '://' + request.get_host()
        data = [{
            'price_data': {
                'currency': 'rub',
                'product_data': product.get_data(),
                'unit_amount': product.price, # TODO: wtf, what's the differebce between "unit_amount" and "quantity"
            },
            'quantity': amount,
        }]
        
        session = stripe.checkout.Session.create(
            line_items=data,
            mode='payment',
            success_url=f'{domain}/success',
            cancel_url=f'{domain}/cancel',
        )

        print('Stripe session object')
        print(session)

        return JsonResponse({
            'StripeCheckoutSessionId': session.stripe_id,
        })
    except (TypeError, KeyError) as err:
        return HttpResponseBadRequest(content=err)

def success(request):
    return render(request=request, template_name='products/success.html')


def cancel(request):
    return render(request=request, template_name='products/cancel.html')


class CartView(TemplateView):
    template_name = "products/cart.html"

    def get_context_data(self, *args, **kwargs):
        context = super(CartView, self).get_context_data(*args, **kwargs)
        context['products'] = Cart.objects.all()

        return context