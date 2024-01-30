from django.shortcuts import render
from .models import *
from django.http import JsonResponse
import json
import datetime
from .util import cookieCart, cartData, guestOrder


# Create your views here.


def sklep(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/sklep.html', context)


def koszyk(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/koszyk.html', context)


def checkout(request):
    data = cartData(request)
    items = data['items']
    order = data['order']
    cartItems = data['cartItems']

    context = {'items': items, 'order': order, 'cartItems': cartItems}
    return render(request, 'store/checkout.html', context)


def kontakt(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/kontakt.html', context)


def blog(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/blog.html', context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data['productId']
    action = data['action']

    print('Action:', action)
    print('ProductId:', productId)

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

    return JsonResponse('Produkt dodano do koszyka', safe=False)


def processOrder(request):
    print('Data:', request.body)
    transaction_id = datetime.datetime.now().time()
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
            region=data['shipping']['state'],
            zipcode=data['shipping']['zipcode'],

        )

    return JsonResponse('Platnosc udana', safe=False)
