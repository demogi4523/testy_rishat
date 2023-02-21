from django.urls import path 
from django.conf.urls.static import static
from django.conf import settings

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
    login_request as login,
    logout,
    account_settings,
    cart,
    orders,
)


urlpatterns = [
    path('', ItemListView.as_view(), name='root'),
    path('register/', register, name='register'),
    path('login/', login, name='login'),
    path("logout", logout, name="logout"),
    path("account-settings", account_settings, name="account-settings"),
    path('get_pk', get_pk, name='get-public-key'),
    path('item/<int:pk>', create_checkout_session, name='ccs'),
    path('items/<int:pk>', ItemView.as_view(), name='item'),
    path('success', success, name='item-buy-success'),
    path('cancel', cancel, name='item-buy-cancel'),
    path('cart', cart, name='cart'),
    path('orders', orders, name='orders'),
]

urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
