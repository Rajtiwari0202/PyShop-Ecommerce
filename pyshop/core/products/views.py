from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product, Cart, CartItem, Order, OrderItem


# ================= AUTH =================

def signup_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        if User.objects.filter(username=username).exists():
            messages.error(request, "User already exists")
            return redirect('signup')

        user = User.objects.create_user(username=username, password=password)
        login(request, user)
        return redirect('product_list')

    return render(request, 'signup.html')


def login_view(request):
    if request.method == "POST":
        username = request.POST['username']
        password = request.POST['password']

        user = authenticate(request, username=username, password=password)

        if user:
            login(request, user)
            return redirect('product_list')
        else:
            messages.error(request, "Invalid credentials")

    return render(request, 'login.html')


def logout_view(request):
    logout(request)
    return redirect('product_list')


# ================= PRODUCTS =================

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})


# ================= CART =================

@login_required
def cart_view(request):
    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.all()
    total_price = cart.total_price()

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)

    cart, created = Cart.objects.get_or_create(user=request.user)

    cart_item, created = CartItem.objects.get_or_create(
        cart=cart,
        product=product
    )

    if not created:
        cart_item.quantity += 1
        cart_item.save()

    return redirect('cart')


@login_required
def remove_from_cart(request, id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=id)

    CartItem.objects.filter(cart=cart, product=product).delete()

    return redirect('cart')


@login_required
def increase_quantity(request, id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=id)

    item = CartItem.objects.get(cart=cart, product=product)
    item.quantity += 1
    item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, id):
    cart = Cart.objects.get(user=request.user)
    product = get_object_or_404(Product, id=id)

    item = CartItem.objects.get(cart=cart, product=product)

    item.quantity -= 1

    if item.quantity <= 0:
        item.delete()
    else:
        item.save()

    return redirect('cart')


# ================= CHECKOUT =================

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    if cart.items.count() == 0:
        return redirect('cart')

    total = cart.total_price()

    if request.method == "POST":
        # Create Order
        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status="Completed"
        )

        # Copy items
        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        # Clear cart
        cart.items.all().delete()

        return render(request, 'success.html', {'total': total})

    return render(request, 'checkout.html', {'total': total})