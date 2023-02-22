import os
import json
from typing import Any

from django.http import HttpRequest, HttpResponseBadRequest
from django.db.models import QuerySet
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http.response import JsonResponse
from django.views.decorators import http
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import stripe
from dotenv import load_dotenv, find_dotenv

from products.models import Item, Cart, Order, Tax


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

def success(request: HttpRequest):
    return render(request=request, template_name='products/success.html')


def cancel(request: HttpRequest):
    return render(request=request, template_name='products/cancel.html')


@login_required
def clean(request: HttpRequest):
    current_user = request.user
    current_user_cart = Cart.objects.get(user=current_user)
    current_user_cart.clear()

    return redirect('root')


class OrderListView(ListView):
    model = Order
    context_object_name = "orders"

    def get_queryset(self) -> QuerySet[Any]:
        return Order.objects.filter(user=self.request.user)


@http.require_GET
@login_required
def create_cart_checkout_session(request: HttpRequest, pk: int):
    # try:
    print(pk)
    order = Order.objects.get(pk=pk)
    
    domain = request.scheme + '://' + request.get_host()
    # data = [{
    #     'price_data': {
    #         'currency': 'rub',
    #         'product_data': product.get_data(),
    #         'unit_amount': product.price, # TODO: wtf, what's the differebce between "unit_amount" and "quantity"
    #     },
    #     'quantity': amount,
    # }]
    data = []
    items = order.get_items()
    for item in items:
        percent = Tax.objects.get(pk=item.item.pk).percent

        tax_rate = stripe.TaxRate.create( # Here
            display_name=f'Sales Tax for item #{item.item.pk}',
            percentage=percent,
            inclusive=True 
        )

        data_el = {
            'price_data': {
                'unit_amount': item.item.price,
                'currency': 'rub',
                'product_data': item.item.get_data()
            },
            'quantity': item.quantity,
            'tax_rates': [tax_rate['id']] # Here
        }
    # if item.item.discount:
    #     data_el['discount'] = item.item.discount
    data.append(data_el)

    session = stripe.checkout.Session.create(
        line_items=data,
        mode='payment',
        automatic_tax={
            'enabled': True,
        },
        customer_email = request.user.email,
        success_url=f'{domain}/success',
        cancel_url=f'{domain}/cancel',
    )

    print('Stripe session object')
    print(session)

    return JsonResponse({
        'StripeCheckoutSessionId': session.stripe_id,
    })
    # except (TypeError, KeyError) as err:
    #     return HttpResponseBadRequest(content=err)


@login_required
@http.require_POST
def order(req: HttpRequest, pk:int):
    order = Order.objects.get(pk=pk)
    items = order.get_items()
    data = []
    for item in items:
        data_el = {
            'name': item.item.name,
            'description': item.item.description,
            'price': item.item.price,
            'tax': item.item.tax,
            'quantity': item.quantity,
        }
        if item.item.discount:
            data_el['discount'] = item.item.discount
        data.append(data_el)
    return JsonResponse({
        'items': data,
    })
