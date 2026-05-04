from django.shortcuts import render, get_object_or_404, redirect
from .models import Product

# ✅ Helper function (important abstraction)
def get_cart(request):
    cart = request.session.get('cart', {})

    # Fix old buggy data (list → dict)
    if isinstance(cart, list):
        new_cart = {}
        for pid in cart:
            pid = str(pid)
            new_cart[pid] = new_cart.get(pid, 0) + 1
        cart = new_cart
        request.session['cart'] = cart

    return cart


def product_list(request):
    products = Product.objects.all()
    return render(request, 'products/product_list.html', {'products': products})


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)
    return render(request, 'products/product_detail.html', {'product': product})


# ✅ Add to cart
def add_to_cart(request, id):
    cart = get_cart(request)
    id = str(id)

    cart[id] = cart.get(id, 0) + 1
    request.session['cart'] = cart

    return redirect('cart')


# ✅ Increase quantity
def increase_quantity(request, id):
    cart = get_cart(request)
    id = str(id)

    if id in cart:
        cart[id] += 1

    request.session['cart'] = cart
    return redirect('cart')


# ✅ Decrease quantity
def decrease_quantity(request, id):
    cart = get_cart(request)
    id = str(id)

    if id in cart:
        cart[id] -= 1
        if cart[id] <= 0:
            del cart[id]

    request.session['cart'] = cart
    return redirect('cart')


# ✅ Remove item completely
def remove_from_cart(request, id):
    cart = get_cart(request)
    id = str(id)

    if id in cart:
        del cart[id]

    request.session['cart'] = cart
    return redirect('cart')


# ✅ Clear cart
def clear_cart(request):
    request.session['cart'] = {}
    return redirect('cart')


# ✅ Cart view
def cart(request):
    cart = get_cart(request)

    products = []
    total_price = 0

    for product_id, quantity in cart.items():
        product = get_object_or_404(Product, id=product_id)

        product.quantity = quantity
        product.total = product.price * quantity

        total_price += product.total
        products.append(product)

    return render(request, 'products/cart.html', {
        'products': products,
        'total_price': total_price
    })