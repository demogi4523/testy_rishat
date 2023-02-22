from django.urls import path 
from django.conf.urls.static import static
from django.conf import settings
from django.contrib.auth.decorators import login_required

from products.views import (
    ItemListView, 
    ItemView,
    get_pk, 
    create_checkout_session,
    success,
    cancel,
    OrderListView,
    order,
    create_cart_checkout_session
)
from custom_auth.views import (
    register,
    login_request as login,
    logout,
    account_settings,
    CartView,
    make_order,
)


urlpatterns = [
    path('', ItemListView.as_view(), name='root'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path("logout", logout, name="logout"),
    path("account_settings", account_settings, name="account-settings"),
    path('get_pk', get_pk, name='get-public-key'),
    path('item/<int:pk>', create_checkout_session, name='ccs'),
    path('items/<int:pk>', ItemView.as_view(), name='item'),
    path('success', success, name='item-buy-success'),
    path('cancel', cancel, name='item-buy-cancel'),
    path('cart', login_required(CartView.as_view()), name='cart'),
    path('orders', login_required(OrderListView.as_view()), name='orders'),
    path('orders/<int:pk>', create_cart_checkout_session, name='order'),
    path('make_order', make_order, name='make-order'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
