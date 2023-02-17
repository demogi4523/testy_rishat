import os

from django.views.generic.detail import DetailView
from django.views.generic.list import ListView
from django.http.response import JsonResponse
from django.views.decorators import http
from django.shortcuts import redirect, render
from django.conf import settings
import stripe
from dotenv import load_dotenv, find_dotenv

from products.models import Item


class ItemListView(ListView):
    model = Item


# TODO:
# -	GET /buy/{id}, c помощью которого можно получить Stripe Session Id для оплаты выбранного Item. 
#   При выполнении этого метода c бэкенда с помощью python библиотеки stripe должен выполняться запрос 
#   stripe.checkout.Session.create(...) и полученный session.id выдаваться в результате запроса
# 
# -	GET /item/{id}, c помощью которого можно получить простейшую HTML страницу, 
#   на которой будет информация о выбранном Item и кнопка Buy. 
#   По нажатию на кнопку Buy должен происходить запрос на /buy/{id}, 
#   получение session_id и далее  с помощью JS библиотеки Stripe 
#   происходить редирект на Checkout форму stripe.redirectToCheckout(sessionId=session_id)
class ItemView(DetailView):
    model = Item

@http.require_GET
def buy_item(request, pk):
    data = Item.objects.get(pk=pk)
    print(data)
    data = data.serialize()
    return render(request=request, template_name='products/checkout.html', context=data)

load_dotenv(find_dotenv())
stripe.api_key = os.environ['STRIPE_API_SECRET_KEY']

def get_pk(request):
    pk_key = os.environ['STRIPE_API_PUBLIC_KEY']
    return JsonResponse({
        "pk": pk_key,
    })

@http.require_POST
def create_checkout_session(request, pk):
    # data = json.loads(request.body)
    # pk = data.pk
    # amount = data.amount
    product = Item.objects.get(pk=pk)

    # FIXME: fix this hardcoded domain
    domain = 'http://localhost:8000'
    data = [{
        'price_data': {
            'currency': 'rub',
            'product_data': product.get_data(),
            'unit_amount': product.price, # TODO: wtf, what's the differebce between "unit_amount" and "quantity"
        },
        'quantity': 1,
    }]
    print(data)
    
    session = stripe.checkout.Session.create(
        line_items=data,
        mode='payment',
        success_url=f'{domain}/success',
        cancel_url=f'{domain}/cancel',
    )

    return redirect(session.url, code=303)


def success(request):
    return render(request=request, template_name='products/success.html')


def cancel(request):
    return render(request=request, template_name='products/cancel.html')