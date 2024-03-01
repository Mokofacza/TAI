from .models import *
from django.http import JsonResponse, HttpResponse
import json
import datetime
from .util import cartData, guestOrder
from django.shortcuts import render, redirect, get_object_or_404
from .forms import *
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import *


# Create your views here.

def sklep(request):
    data = cartData(request)
    cartItems = data['cartItems']
    products = Product.objects.all()

    context = {'products': products, 'cartItems': cartItems}
    return render(request, 'store/sklep.html', context)


@api_view(['GET'])
def sklep_api(request):
    data = cartData(request)
    cartItems = data['cartItems']

    products = Product.objects.all()
    products_serializer = ProductSerializer(products, many=True)

    return Response({'products': products_serializer.data, 'cartItems': cartItems})


def sklep_test(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/sklep_testowy.html', context)


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
    posts = BlogPost.objects.all()

    if request.method == 'POST':
        form = KomentarzForm(request.POST)
        if form.is_valid() and request.user.is_authenticated:
            blogpost_id = form.cleaned_data.get('blogpost_id')
            blogpost = get_object_or_404(BlogPost, id=blogpost_id)
            komentarz = form.save(commit=False)
            komentarz.user = request.user
            komentarz.blogpost = blogpost
            komentarz.save()
            print(f"ID komentarza: {komentarz.id}")
            return redirect('blog')
    else:
        form = KomentarzForm()

    context = {'posts': posts, 'cartItems': cartItems, 'form': form}
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
        print(f"Customer: {customer}, order: {order, created}")

    else:
        customer, order = guestOrder(request, data)
        print(f"Customer: {customer}, order: {order}")

    total = float(data['form']['total'])
    order.transaction_id = transaction_id
    print(total)
    print(order.get_cart_total)

    if total == float(order.get_cart_total):
        order.complete = True
        print(order.complete)

    print(f"Podsumwowanioe: {order}")

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


def register(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save()
            Customer.objects.create(user=user, name=user.username, email=user.email)
            return redirect('login')
    else:
        form = RegisterForm()
    return render(request, 'store/register.html', {'register_form': form})


def random_meal(request):
    data = cartData(request)
    cartItems = data['cartItems']

    context = {'cartItems': cartItems}
    return render(request, 'store/meal.html', context)


def usun_komentarz(request, komentarz_id):
    komentarz = get_object_or_404(Komentarz, id=komentarz_id)

    if request.user != komentarz.user and not request.user.is_staff:
        return HttpResponse('Nie masz uprawnień do usunięcia tego komentarza.', status=403)
    else:
        komentarz.delete()
    return redirect('blog')


@api_view(['GET'])
def getData(request):
    person = {'name': 'TAI'}
    return Response(person)


def panel_admina(request):
    if not request.user.is_authenticated or not request.user.is_staff:
        return redirect('sklep')

    if request.method == 'POST':
        form = BlogPostForm(request.POST, request.FILES)
        if form.is_valid():
            blog_post = form.save(commit=False)
            blog_post.author = request.user
            blog_post.save()
            return redirect('panel_admina')
    else:
        form = BlogPostForm()

    data = cartData(request)
    cartItems = data['cartItems']

    orders = Order.objects.all().order_by('-date_ordered')

    context = {
        'cartItems': cartItems,
        'form': form,
        'orders': orders
    }
    return render(request, 'store/admin.html', context)


def delete_post(request, post_id):
    if request.user.is_authenticated and request.user.is_staff:
        post = get_object_or_404(BlogPost, id=post_id)
        post.delete()
    return redirect('blog')
