from django.shortcuts import render, redirect
from .models import *
from django.http import JsonResponse
import datetime
import json
from .utils import cookieCart, cartData, guestOrder
from django.core.paginator import Paginator
from .models import Product 
from django.views import View
from .forms import NewUserForm
from django.contrib.auth import login, logout
from django.contrib import messages
from django.contrib.auth import login, authenticate #add this
from django.contrib.auth.forms import AuthenticationForm #add this


 # Create your views here.


def landingPage(request):
    return render(request, 'store/landingPage.html')

def bookTable(request):
    return render(request, 'store/bookTable.html')


def contactPage(request):
    return render(request, 'store/contactPage.html')

class CategoryView(View):
    def get(self, request, val):
        product = Product.objects.filter(category=val)
        name = Product.objects.filter(category=val)
        data = cartData(request)
        cartItems = data['cartItems']
        order = data['order']
        products = Product.objects.all()
        return render(request, 'store/category.html', locals())


def shop(request):
    products = Product.objects.all()
    paginator = Paginator(products, 12)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)

    data = cartData(request)
    cartItems = data['cartItems']
    context = {'products' : products, 'cartItems' : cartItems, 'product' : page_obj}
    return  render(request, 'store/store.html', context)


def cart(request):
    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items'] 
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
    return  render(request, 'store/cart.html', context)


def checkout(request):

    data = cartData(request)
    cartItems = data['cartItems']
    order = data['order']
    items = data['items']
    
    context = {'items' : items, 'order' : order, 'cartItems' : cartItems}
    return  render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('Product:', productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    
    if action == 'add':
	    orderItem.quantity = (orderItem.quantity + 1)
    elif action == 'remove':
	    orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was Added', safe=False)


def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:   
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)

    else:
        customer, order = guestOrder(request, data)

    total = float(data['form']['total'])
    order.transaction_id = transaction_id

    if total == order.get_cart_total:
        order.complete = True
    order.save()

    if order.shipping == True:
            ShippingAddress.objects.create(
            customer=customer,
            order=order,
            address=data['shipping']['address'],
            city=data['shipping']['city'],
            state=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],
            )
    return JsonResponse('Payment submitted..', safe=False)

def register_request(request):
    if request.method == "POST":
	    form = NewUserForm(request.POST)
	    if form.is_valid():
		    user = form.save()
		    login(request, user)
		    messages.success(request, "Registration successful." )
		    return redirect("shop")
	    messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    context = {"register_form" : form}
    return render (request, "store/register.html", context)


def login_request(request):
    if request.method == "POST":
	    form = AuthenticationForm(request, data=request.POST)
	    if form.is_valid():
		    username = form.cleaned_data.get('username')
		    password = form.cleaned_data.get('password')
		    user = authenticate(username=username, password=password)
		    if user is not None:
			    login(request, user)
			    messages.info(request, f"You are now logged in as {username}.")
			    return redirect("shop")
		    else:
			    messages.error(request,"Invalid username or password.")
	    else:
		    messages.error(request,"Invalid username or password.")
    form = AuthenticationForm()
    context = {"login_form": form}
    return render(request, "store/login.html", context)


def logout_request(request):
	logout(request)
	messages.info(request, "You have successfully logged out.") 
	return redirect("shop")