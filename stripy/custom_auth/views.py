from django.http import HttpRequest, HttpResponse
from django.shortcuts import  render, redirect
from django.contrib.auth import login, authenticate, logout as lgt
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.contrib.auth.forms import AuthenticationForm

from django.views.decorators.http import require_http_methods

from custom_auth.models import Avatar
from custom_auth.forms import UserRegistrationForm, AccountPhotoUpdateForm

def register(request: HttpRequest):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(user_form.cleaned_data['password'])
            # Save the User object
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
				# return redirect("main:homepage")
				return redirect("/")
			else:
				messages.error(request,"Invalid username or password.")
		else:
			messages.error(request,"Invalid username or password.")
	form = AuthenticationForm()
	return render(request=request, template_name="account/login.html", context={"login_form":form})


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
            print(photo)
            avatar = Avatar.objects.get(user=req.user)
            avatar.photo = photo
            avatar.save()
            return HttpResponse("OK")
        return HttpResponse("Wrong!", 405)
    

@login_required
def logout(req: HttpRequest):
    lgt(req)
    return redirect('root')


def cart(req: HttpRequest):
      pass


def orders(req: HttpRequest):
      pass
