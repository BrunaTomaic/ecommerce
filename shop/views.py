from django.shortcuts import render, redirect
from django.http import JsonResponse
import json
import datetime
from .models import *
from django.http import HttpResponse
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from .forms import CreateUserForm

# imports for REST API
from rest_framework.decorators import api_view
from rest_framework.response import Response
from .serializers import ProductSerializer
from .models import Product


@api_view(["GET"])
def apiOverview(request):
    api_urls = {
        "List": "/product-list/",
        "Detail View": "/product-detail/<str:pk>/",
        "Create": "/product-create/",
        "Update": "/product-update/<str:pk>/",
        "Delete": "/product-delete/<str:pk>/",
    }

    return Response(api_urls)


@api_view(["GET"])
def productList(request):
    product = Product.objects.all().order_by("-id")
    serializer = ProductSerializer(product, many=True)
    return Response(serializer.data)


# @api_view(["GET"])
# def productDetail(request, pk):
#     product = Product.objects.get(id=pk)
#     serializer = ProductSerializer(product, many=False)
#     return Response(serializer.data)


# @api_view(["POST"])
# def productCreate(request):
#     serializer = ProductSerializer(data=request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(["POST"])
# def productUpdate(request, pk):
#     product = Product.objects.get(id=pk)
#     serializer = ProductSerializer(instance=product, data=request.data)

#     if serializer.is_valid():
#         serializer.save()

#     return Response(serializer.data)


# @api_view(["DELETE"])
# def productDelete(request, pk):
#     product = Product.objects.get(id=pk)
#     product.delete()

#     return Response("Item succsesfully delete!")


def signup(request):

    form = CreateUserForm()
    if request.method == "POST":
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get("username")

            messages.success(request, "Account was created for " + username)

            return redirect("shop")

    context = {"form": form}
    return render(request, "registration/signup.html", context)


# def shop(request):

#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#     else:
#         # Create empty cart for now for non-logged in user
#         items = []
#         order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
#         cartItems = order["get_cart_items"]

#     products = Product.objects.all()
#     context = {"products": products, "cartItems": cartItems}
#     return render(request, "shop/shop.html", context)


# def shop(request):

#     if request.user.is_authenticated:
#         customer = request.user.customer
#         order, created = Order.objects.get_or_create(customer=customer, complete=False)
#         items = order.orderitem_set.all()
#         cartItems = order.get_cart_items
#     else:
#         # Create empty cart for now for non-logged in user
#         items = []
#         order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
#         cartItems = order["get_cart_items"]

#     products = Product.objects.all()
#     context = {"products": products, "cartItems": cartItems}
#     return render(request, "shop/shop.html", context)


def shop(request):
    return render(request, "shop/shop.html")


def cart(request):

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "shop/cart.html", context)


def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        # Create empty cart for now for non-logged in user
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0, "shipping": False}
        cartItems = order["get_cart_items"]

    context = {"items": items, "order": order, "cartItems": cartItems}
    return render(request, "shop/checkout.html", context)


def updateItem(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]
    print("Action:", action)
    print("Product:", productId)

    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse("Item was added", safe=False)


from django.views.decorators.csrf import csrf_exempt


@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data["form"]["total"])
        order.transaction_id = transaction_id

        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(
                customer=customer,
                order=order,
                address=data["shipping"]["address"],
                city=data["shipping"]["city"],
                zipcode=data["shipping"]["zipcode"],
            )
    else:
        print("User is not logged in")

    return JsonResponse("Payment submitted..", safe=False)
