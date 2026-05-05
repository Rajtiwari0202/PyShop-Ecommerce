from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required

from .models import Product, Cart, CartItem, Order, OrderItem,Wishlist
# (Add Wishlist later when we implement it)


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
    query = request.GET.get('q')

    if query:
        products = Product.objects.filter(name__icontains=query)
    else:
        products = Product.objects.all()

    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})


# ================= CART =================

@login_required
def cart_view(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    cart_items = cart.items.all()
    total_price = cart.total_price()

    return render(request, 'products/cart.html', {
        'cart_items': cart_items,
        'total_price': total_price
    })


@login_required
def add_to_cart(request, id):
    product = get_object_or_404(Product, id=id)
    cart, _ = Cart.objects.get_or_create(user=request.user)

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
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=id)

    CartItem.objects.filter(cart=cart, product=product).delete()
    return redirect('cart')


@login_required
def increase_quantity(request, id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=id)

    item = CartItem.objects.filter(cart=cart, product=product).first()

    if item:
        item.quantity += 1
        item.save()

    return redirect('cart')


@login_required
def decrease_quantity(request, id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=id)

    item = CartItem.objects.filter(cart=cart, product=product).first()

    if item:
        item.quantity -= 1

        if item.quantity <= 0:
            item.delete()
        else:
            item.save()

    return redirect('cart')


# ================= CHECKOUT =================

@login_required
def checkout(request):
    cart, _ = Cart.objects.get_or_create(user=request.user)

    if cart.items.count() == 0:
        return redirect('cart')

    total = cart.total_price()

    if request.method == "POST":
        payment_method = request.POST.get('payment', 'cod')

        order = Order.objects.create(
            user=request.user,
            total_amount=total,
            status=f"Placed ({payment_method.upper()})"
        )

        for item in cart.items.all():
            OrderItem.objects.create(
                order=order,
                product=item.product,
                quantity=item.quantity,
                price=item.product.price
            )

        cart.items.all().delete()

        return render(request, 'success.html', {
            'total': total,
            'payment_method': payment_method
        })

    return render(request, 'checkout.html', {'total': total})


# ================= ORDERS =================

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'products/order_history.html', {
        'orders': orders
    })

@login_required
def add_to_wishlist(request, id):
    if request.method == "POST":
        product = get_object_or_404(Product, id=id)
        Wishlist.objects.get_or_create(user=request.user, product=product)

    return redirect('product_list')
@login_required
def remove_from_wishlist(request, id):
    product = get_object_or_404(Product, id=id)
    Wishlist.objects.filter(user=request.user, product=product).delete()
    return redirect('wishlist')

@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'products/wishlist.html', {
        'items': items
    })