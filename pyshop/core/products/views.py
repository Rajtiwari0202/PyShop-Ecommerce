from django.shortcuts import render, get_object_or_404, redirect
from .models import Product
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

@login_required
def checkout(request):
    cart = request.session.get('cart', {})

    if not cart:
        return redirect('cart')

    total = 0
    for product_id, qty in cart.items():
        product = Product.objects.get(id=product_id)
        total += product.price * qty

    if request.method == "POST":
        # Fake payment success
        request.session['cart'] = {}
        return render(request, 'success.html', {'total': total})

    return render(request, 'checkout.html', {'total': total})
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

def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})


def add_to_cart(request, id):
    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    id = str(id)

    cart[id] = cart.get(id, 0) + 1

    request.session['cart'] = cart
    request.session.modified = True

    return redirect('cart')


def remove_from_cart(request, id):
    cart = request.session.get('cart', {})

    id = str(id)
    if id in cart:
        del cart[id]

    request.session['cart'] = cart
    return redirect('cart')


def increase_quantity(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        cart[id] += 1

    request.session['cart'] = cart
    return redirect('cart')


def decrease_quantity(request, id):
    cart = request.session.get('cart', {})
    id = str(id)

    if id in cart:
        cart[id] -= 1

        if cart[id] <= 0:
            del cart[id]

    request.session['cart'] = cart
    return redirect('cart')


def cart(request):
    cart = request.session.get('cart', {})

    if not isinstance(cart, dict):
        cart = {}

    cart_items = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        subtotal = product.price * quantity
        total_price += subtotal

        cart_items.append({
            'product': product,
            'quantity': quantity,
            'subtotal': subtotal
        })

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })