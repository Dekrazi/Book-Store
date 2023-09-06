from django.contrib.auth.forms import UserCreationForm, AuthenticationForm
from django.contrib.auth import authenticate, login
from django.urls import reverse_lazy
from django.views import generic
from django.shortcuts import render, redirect
from cart.models import Customer
from django.contrib.auth.models import User, Group
from django.contrib.auth.decorators import login_required, user_passes_test
from django import template


register = template.Library()


@register.filter(name="in_group")
def in_group(user, group_name):
    return user.groups.filter(name=group_name).exists()


def user_in_book_store_staff_group(user):
    return user.groups.filter(name="Book Store Staff").exists()


@user_passes_test(
    lambda user: user_in_book_store_staff_group(user) or user.is_superuser
)
def manage_users(request):
    users = User.objects.all()
    groups = Group.objects.all()

    if request.method == "POST":
        for group in groups:
            group_id = str(group.id)
            for user in users:
                action = request.POST.get("action")
                user_id = str(user.id)

                if action == f"add_staff_{user_id}":
                    user = User.objects.get(id=user_id)
                    group = Group.objects.get(name="Book Store Staff")
                    group.user_set.add(user)
                elif action == f"remove_staff_{user_id}":
                    user = User.objects.get(id=user_id)
                    group = Group.objects.get(name="Book Store Staff")
                    group.user_set.remove(user)

        return redirect(request.path)

    for group in groups:
        group.users = group.user_set.all()

    return render(request, "manage_users.html", {"groups": groups, "users": users})


# Create your views here.
class SignUpView(generic.CreateView):
    form_class = UserCreationForm
    success_url = reverse_lazy("login")
    template_name = "signup.html"


def login_view(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data["username"]
            password = form.cleaned_data["password"]
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)

                # Check if a Customer object exists for the user
                customer, created = Customer.objects.get_or_create(
                    user=user, defaults={"name": user.username}
                )

                return redirect("books")
    else:
        form = AuthenticationForm()

    return render(request, "registration/login.html", {"form": form})


def user_info(request):
    return render(request, "user_info.html")
