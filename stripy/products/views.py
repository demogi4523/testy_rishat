import os
import json
from typing import Any

from django.http import HttpRequest, HttpResponseBadRequest, HttpResponse
from django.db.models import QuerySet
from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.views.decorators.csrf import csrf_exempt
from django.http.response import JsonResponse
from django.views.decorators import http
from django.contrib.auth.decorators import login_required
from django.shortcuts import render, redirect
import stripe
from dotenv import load_dotenv, find_dotenv

from products.models import (
    Item, 
    Cart, 
    Order, 
    # Tax, 
    Discount,
)


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
                'unit_amount': product.price,
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
    try:
        order = Order.objects.get(pk=pk)
        domain = request.scheme + '://' + request.get_host()
        data = []
        items = order.get_items()
        # print(items)
        # discounts = []

        for item in items:
            # percent = Tax.objects.get(pk=item.item.pk).percent

            # tax_rate = stripe.TaxRate.create( # Here
            #     display_name=f'Sales Tax for item #{item.item.pk}',
            #     percentage=percent,
            #     inclusive=True 
            # )

            # discount_pk = item.item.pk
            # try:
            #     discount = Discount.objects.get(pk=discount_pk)
            #     percent = discount.percent
            #     COUPON_ID = stripe.Coupon.create(percent_off=percent, duration="once")

            #     discount = {
            #         'coupon': COUPON_ID,
            #     }
            #     discounts.append(discount)
            # except Discount.DoesNotExist as err:
            #     print(err)
            
            data_el = {
                'price_data': {
                    'unit_amount': item.item.price,
                    'currency': 'rub',
                    'product_data': item.item.get_data()
                },
                'quantity': item.quantity,
                # 'tax_rates': [tax_rate['id']] # Here
            }

            data.append(data_el)

        # print(data)
        # print()
        # print(discounts)

        session = stripe.checkout.Session.create(
            line_items=data,
            mode='payment',
            # discounts=discounts,
            # automatic_tax={
            #     'enabled': True,
            # },
            customer_email = request.user.email,
            success_url=f'{domain}/success',
            cancel_url=f'{domain}/cancel',
        )

        # print('Stripe session object')
        order.stripe_checkout_session_id = session.stripe_id
        order.save()

        return JsonResponse({
            'StripeCheckoutSessionId': session.stripe_id,
        })
    except (TypeError, KeyError) as err:
        return HttpResponseBadRequest(content=err)


@csrf_exempt # only for testing, you need proper auth in production
def webhook(req: HttpRequest):
    try:
        payload = req.body
        event = json.loads(payload)
    except ValueError as e:
        print("⚠️ Webhook error while parsing basic request." + str(e))
        return JsonResponse({"success": True}, status=400)

    # Handling a subscription being cancelled on the dashboard
    if event and event["type"] == "checkout.session.completed":
        print("checkout.session.completed") # log event
        # print(event) # log event
        stripe_checkout_session_id = event["data"]["object"]["id"]
        try:
            order = Order.objects.get(stripe_checkout_session_id=stripe_checkout_session_id)
            order.mark_payed()
            order.save()
        except Order.DoesNotExist as err:
            print(err)

        
    if event and event["type"] == "checkout.session.expire":
        print("checkout.session.expire") # log event
        print(event) # log event

    
    return HttpResponse(200)


@http.require_POST
@login_required
def card_add(req: HttpRequest):
    try:
        data = json.loads(req.body)
        item_pk = data["pk"]
        amount = data["amount"]
        cart = Cart.objects.get(user=req.user)
        item = Item.objects.get(pk=item_pk)
        cart.add_item(item, amount)
        return HttpResponse(200)
    except Exception as err:
        print(err)
        return HttpResponseBadRequest()