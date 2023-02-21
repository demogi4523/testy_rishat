from django.urls import path

from products.views import (
    ItemListView, 
    ItemView,
    get_pk, 
    create_checkout_session,
    success,
    cancel,
)
from custom_auth.views import (
    register,
    login_request as login
)


urlpatterns = [
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path('', ItemListView.as_view(), name='items'),
    path('items/<int:pk>', ItemView.as_view(), name='item'),
    path('get_pk', get_pk, name='get-public-key'),
    path('item/<int:pk>', create_checkout_session, name='ccs'),
    path('success', success, name='item-buy-success'),
    path('cancel', cancel, name='item-buy-cancel'),
]

