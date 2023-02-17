from django.urls import path

from products.views import (
    ItemListView, 
    ItemView, 
    buy_item, 
    get_pk, 
    create_checkout_session,
    success,
    cancel,
)


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
urlpatterns = [
    path('', ItemListView.as_view(), name='items'),
    path('items/<int:pk>', ItemView.as_view(), name='item'),
    path('buy/<int:pk>', buy_item, name='item-buy'),
    path('get_pk', get_pk, name='get-public-key'),
    path('create_checkout_session/<int:pk>', create_checkout_session, name='ccs'),
    path('success', success, name='item-buy-success'),
    path('cancel', cancel, name='item-buy-cancel'),
]

