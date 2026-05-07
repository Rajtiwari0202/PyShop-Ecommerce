from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth.decorators import login_required
import razorpay
from django.http import HttpResponse
from reportlab.pdfgen import canvas
from django.conf import settings
from .models import Product, Cart, CartItem, Order, OrderItem, Wishlist, Category

import json
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt

@csrf_exempt
@login_required
def verify_payment(request):
    if request.method == "POST":
        data = json.loads(request.body)

        razorpay_payment_id = data.get("razorpay_payment_id")
        razorpay_order_id = data.get("razorpay_order_id")
        razorpay_signature = data.get("razorpay_signature")

        client = razorpay.Client(auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET))

        try:
            client.utility.verify_payment_signature({
                'razorpay_order_id': razorpay_order_id,
                'razorpay_payment_id': razorpay_payment_id,
                'razorpay_signature': razorpay_signature
            })

            # ✅ Signature valid → create order
            cart = Cart.objects.get(user=request.user)

            order = Order.objects.create(
                user=request.user,
                total_amount=cart.total_price(),
                status="Confirmed",
                razorpay_payment_id=razorpay_payment_id
            )

            for item in cart.items.all():
                OrderItem.objects.create(
                    order=order,
                    product=item.product,
                    quantity=item.quantity,
                    price=item.product.price
                )

            cart.items.all().delete()

            return JsonResponse({"status": "success"})

        except razorpay.errors.SignatureVerificationError:
            return JsonResponse({"status": "failed", "message": "Invalid signature"})

        except Exception as e:
            return JsonResponse({"status": "error", "message": str(e)})
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
    category_id = request.GET.get('category')
    min_price = request.GET.get('min_price')
    max_price = request.GET.get('max_price')

    products = Product.objects.all()
    categories = Category.objects.all()
    wishlist_items = []

    if request.user.is_authenticated:
        wishlist_items = Wishlist.objects.filter(user=request.user)\
            .values_list('product_id', flat=True)

    # 🔍 Search
    if query:
        products = products.filter(name__icontains=query)

    # 📂 Category filter
    if category_id:
        products = products.filter(category_id=category_id)

    # 💰 Price filter
    if min_price:
        products = products.filter(price__gte=min_price)

    if max_price:
        products = products.filter(price__lte=max_price)

    return render(request, 'products/product_list.html', {
        'products': products,
        'categories': categories,
        'wishlist_items': wishlist_items
    })


def product_detail(request, id):
    product = get_object_or_404(Product, id=id)

    # OPTIONAL: show related products (good UX)
    related_products = Product.objects.filter(
        category=product.category
    ).exclude(id=product.id)[:4]

    return render(request, 'products/product_detail.html', {
        'product': product,
        'related_products': related_products
    })


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

    messages.success(request, f"{product.name} added to cart")
    return redirect('cart')


@login_required
def remove_from_cart(request, id):
    cart, _ = Cart.objects.get_or_create(user=request.user)
    product = get_object_or_404(Product, id=id)

    CartItem.objects.filter(cart=cart, product=product).delete()
    messages.warning(request, f"{product.name} removed from cart")
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
            messages.warning(request, f"{product.name} removed from cart")
        else:
            item.save()

    return redirect('cart')


# ================= CHECKOUT =================

@login_required
def checkout(request):
    cart = Cart.objects.get(user=request.user)

    if cart.items.count() == 0:
        messages.warning(request, "Your cart is empty")
        return redirect('cart')

    total = int(cart.total_price() * 100)

    client = razorpay.Client(
        auth=(settings.RAZORPAY_KEY_ID, settings.RAZORPAY_KEY_SECRET)
    )

    payment = client.order.create({
        "amount": total,
        "currency": "INR",
        "payment_capture": "1"
    })

    return render(request, "products/payment.html", {
        "payment": payment,
        "total": total // 100,
        "razorpay_key": settings.RAZORPAY_KEY_ID
    })


# ================= ORDERS =================

@login_required
def order_history(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')

    return render(request, 'products/order_history.html', {
        'orders': orders
    })


# ================= WISHLIST =================

@login_required
def add_to_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    Wishlist.objects.get_or_create(user=request.user, product=product)

    messages.success(request, f"{product.name} added to wishlist")
    return redirect('product_list')


@login_required
def remove_from_wishlist(request, id):
    product = get_object_or_404(Product, id=id)

    Wishlist.objects.filter(user=request.user, product=product).delete()

    messages.warning(request, f"{product.name} removed from wishlist")
    return redirect('product_list')  # ✅ FIXED


@login_required
def wishlist_view(request):
    items = Wishlist.objects.filter(user=request.user)

    return render(request, 'products/wishlist.html', {
        'items': items
    })


# ================= PAYMENT SUCCESS =================

@login_required
def payment_success(request):
    return render(request, "products/success.html")

@login_required
def track_order(request, order_id):
    order = get_object_or_404(Order, id=order_id, user=request.user)

    return render(request, 'products/track_order.html', {
        'order': order
    })

# Invoice Download feature
@login_required
def download_invoice(request, order_id):

    order = get_object_or_404(Order, id=order_id, user=request.user)

    response = HttpResponse(content_type='application/pdf')

    response['Content-Disposition'] = f'attachment; filename="invoice_{order.id}.pdf"'

    p = canvas.Canvas(response)

    # HEADER
    p.setFont("Helvetica-Bold", 20)
    p.drawString(200, 800, "PyShop Invoice")

    # ORDER INFO
    p.setFont("Helvetica", 12)

    p.drawString(50, 760, f"Order ID: {order.id}")
    p.drawString(50, 740, f"Customer: {order.user.username}")
    p.drawString(50, 720, f"Status: {order.status}")
    p.drawString(50, 700, f"Date: {order.created_at.strftime('%d-%m-%Y')}")

    # ITEMS HEADER
    p.drawString(50, 650, "Product")
    p.drawString(300, 650, "Qty")
    p.drawString(400, 650, "Price")

    y = 620

    # PRODUCTS
    for item in order.items.all():

        p.drawString(50, y, item.product.name)
        p.drawString(300, y, str(item.quantity))
        p.drawString(400, y, f"₹{item.price}")

        y -= 30

    # TOTAL
    p.setFont("Helvetica-Bold", 14)
    p.drawString(50, y - 20, f"Total Amount: ₹{order.total_amount}")

    p.save()

    return response