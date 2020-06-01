from django.urls import include, path
from . import views

# from rest_framework import routers


urlpatterns = [
    path("", views.shop, name="shop"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("update_item/", views.updateItem, name="update_item"),
    path("process_order/", views.processOrder, name="process_order"),
    path("signup/", views.signup, name="signup"),
    path("product-list/", views.productList, name="product-list"),
    # path("product-detail/<str:pk>/", views.productDetail, name="product-detail"),
    # path("product-create/", views.productCreate, name="product-create"),
    # path("product-update/<str:pk>/", views.productUpdate, name="product-update"),
    # path("product-delete/<str:pk>/", views.productDelete, name="product-delete"),
]
