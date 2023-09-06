from django.urls import path
from . import views

urlpatterns = [
    path("update_item/", views.update_item, name="update-item"),
    path("cart/", views.cart, name="cart"),
    path("checkout/", views.checkout, name="checkout"),
    path("make_payment/", views.make_payment, name="make_payment"),
]
