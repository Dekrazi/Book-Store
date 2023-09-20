from django.shortcuts import render, redirect
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
import json
import os
from .models import Order, OrderItem, Customer
from catalog.models import Book

BASE_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def calculate_cart_totals(items):
    cart_total = sum(item.product.price * item.quantity for item in items)
    quantity_total = sum(item.quantity for item in items)
    return cart_total, quantity_total


def cart(request):
    if request.user.is_authenticated:
        user = request.user
        order, created = Order.objects.get_or_create(user=user, complete=False)
        items = order.orderitem_set.all()

        for item in items:
            item.total_price = item.product.price * item.quantity

        cartItems = order.get_cart_items()  # Calculate cartItems
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]  # Initialize cartItems for anonymous users

    cart_total, quantity_total = calculate_cart_totals(items)
    context = {
        "items": items,
        "cartItems": cartItems,
        "cart_total": cart_total,
        "quantity_total": quantity_total,
    }
    return render(request, "cart.html", context=context)


@login_required
@csrf_exempt
def checkout(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(user=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items()  # Calculate cartItems
    else:
        items = []
        order = {"get_cart_total": 0, "get_cart_items": 0}
        cartItems = order["get_cart_items"]  # Initialize cartItems for anonymous users

    cart_total, quantity_total = calculate_cart_totals(items)  # Calculate cart totals
    context = {
        "items": items,
        "cartItems": cartItems,
        "order": order,
        "cart_total": cart_total,
        "quantity_total": quantity_total,
    }
    context["cart_total"] = cart_total
    return render(request, "checkout.html", context=context)


from django.contrib import messages
from django.http import JsonResponse
import json


@login_required
@csrf_exempt
def update_item(request):
    data = json.loads(request.body)
    productId = data["productId"]
    action = data["action"]

    user = request.user

    # Get the Product instance associated with the selected book
    product = Book.objects.get(id=productId)

    order, created = Order.objects.get_or_create(user=user, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == "add":
        orderItem.quantity = orderItem.quantity + 1
    elif action == "remove":
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    # Add a success message using the messages framework
    messages.success(request, "Book added successfully!")

    return JsonResponse({"message": "Item was updated successfully"})


@login_required
@csrf_exempt
def make_payment(request):
    if request.method == "POST":
        user_info = {
            "name": request.POST.get("name"),
            "email": request.POST.get("email"),
            "address": request.POST.get("address"),
            "city": request.POST.get("city"),
            "state": request.POST.get("state"),
            "zipcode": request.POST.get("zipcode"),
            "country": request.POST.get("country"),
        }

        customer = Customer.objects.get(user=request.user)
        order = Order.objects.get(user=customer.user, complete=False)
        cart_items = order.orderitem_set.all()

        txt_data = f"Name: {user_info['name']}\nEmail: {user_info['email']}\nAddress: {user_info['address']}\nCity: {user_info['city']}\nState: {user_info['state']}\nZipcode: {user_info['zipcode']}\nCountry: {user_info['country']}\n\nCart Contents:\n"

        total_price = 0

        for item in cart_items:
            item_total_price = item.product.price * item.quantity
            txt_data += f"Title: {item.product.title}\nPrice: ${item.product.price}\nQuantity: {item.quantity}\nSubtotal: ${item_total_price}\n\n"
            total_price += item_total_price

        txt_data += f"Total Price to Pay: ${total_price}"

        user_file_name = f"{request.user.username}_user_info.txt"
        payment_info_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "payment_info"
        )
        file_path = os.path.join(payment_info_dir, user_file_name)

        os.makedirs(os.path.dirname(file_path), exist_ok=True)

        try:
            with open(file_path, "w") as txt_file:
                txt_file.write(txt_data)

            order.complete = True
            order.save()

            return redirect(
                "books"
            )  # Replace 'books' with the actual URL name for the books page

        except Exception as e:
            return JsonResponse(
                {"message": f"Error creating TXT file: {str(e)}"}, status=500
            )

    return render(request, "checkout.html")
