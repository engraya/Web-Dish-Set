from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import datetime
import json
from .utils import cookieCart, cartData, guestOrder

from django.core.paginator import Paginator
from .models import Product 

 # Create your views here.

def listing(request):
    product_list = Product.objects.all()
    paginator = Paginator(product_list, 9)

    page_number = request.GET.get('get')
    page_obj = paginator.get_page(page_number)
    context = {'page_obj' : page_obj}
    return render(request, 'store/store.html', context)



def landingPage(request):
    return render(request, 'store/landingPage.html')

def bookTable(request):
    return render(request, 'store/bookTable.html')


def contactPage(request):
    return render(request, 'store/contactPage.html')

def shop(request):

    data = cartData(request)
    cartItems = data['cartItems']
    
    products = Product.objects.all()

    context = {'products' : products, 'cartItems' : cartItems}
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
