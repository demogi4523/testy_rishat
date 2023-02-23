from typing import List

from django.http import HttpRequest, HttpResponse
from django.contrib import messages
from django.contrib.auth import login, authenticate, logout as lgt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm
from django.views.generic.base import TemplateView
from django.views.decorators.http import require_http_methods
from django.shortcuts import  render, redirect
from django.utils.html import escape

from custom_auth.models import Avatar
from custom_auth.forms import UserRegistrationForm, AccountPhotoUpdateForm
from products.models import (
    Cart, 
    CartItem, 
    Order,
    Discount,
)


def register(request: HttpRequest):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            new_user = user_form.save(commit=False)
            new_user.set_password(user_form.cleaned_data['password'])
            new_user.save()
            return render(request, 'account/register_done.html', {'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request, 'account/register.html', {'user_form': user_form})

def login_request(request: HttpRequest):
	if request.method == "POST":
		form = AuthenticationForm(request, data=request.POST)
		if form.is_valid():
			username = form.cleaned_data.get('username')
			password = form.cleaned_data.get('password')
			user = authenticate(username=username, password=password)
			if user is not None:
				login(request, user)
				messages.info(request, f"You are now logged in as {username}.")
				return redirect("root")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="account/login.html", context={"login_form":form})


@login_required
@require_http_methods(["GET", "POST"])
def account_settings(req: HttpRequest):
    # TODO: Crop avatar
    if req.method == "GET":
        form = AccountPhotoUpdateForm()
        return render(
            req,
            "account_settings.html",
            {
                "form": form,
                "prev_photo": Avatar.objects.get(user=req.user).photo.url,
            },
        )
    if req.method == "POST":
        form = AccountPhotoUpdateForm(req.POST, req.FILES)
        if form.is_valid():
            photo = form.cleaned_data["photo"]
            avatar = Avatar.objects.get(user=req.user)
            avatar.photo = photo
            avatar.save()
            return redirect('root')
        return HttpResponse("Wrong!", 405)
    

@login_required
def logout(req: HttpRequest):
    lgt(req)
    return redirect('root')


class CartView(TemplateView):
    template_name = "products/cart.html"

    def get_context_data(self, *args, **kwargs):
        current_user = self.request.user
        current_user_cart = Cart.objects.get(user=current_user)

        context = super(CartView, self).get_context_data(*args, **kwargs)
        print(context)
        items = CartItem.objects.filter(cart=current_user_cart)
        context['items'] = items

        discounts = {}
        for item in items:
            try:
                discount = Discount.objects.get(item=item.item.pk)
                discounts[item.item.pk] = discount.percent
            except Discount.DoesNotExist as err:
                print(err)

        print(discounts)
        context['discounts'] = discounts

        context['summary'] = current_user_cart.summarize()
        print(context)

        return context
    

def make_order(req: HttpRequest):
    #  check all items availability,
    #  create order from cart,
    #  preserve all items
    #  clean cart
    #  and send email
    current_user = req.user
    current_user_cart = Cart.get_cart_by_user(current_user)
    bad_items = []
 
    status = Order.check_items_availability(current_user_cart.get_items(), bad_items)
    if status:
        Order.reserve(current_user_cart)
        Order.create_from_cart(current_user_cart)
        current_user_cart.clear()
        # send_email(order_info)
        return redirect('root')
    else:
         return cancel_order(req, bad_items)


def cancel_order(req: HttpRequest, bad_items: List):
     msg = escape("""
        <ul>
            {}
        </ul>
     """.format("\n".join((
          f"<li><div>{bad_item[0]}</div><div>{bad_item[1]}</div> <div>{bad_item[2]}</div></li>" for bad_item in bad_items
        )))
     )
     messages.add_message(
          request=req,
          level=messages.WARNING,
          message=msg,
     )
     return redirect('cart')    
