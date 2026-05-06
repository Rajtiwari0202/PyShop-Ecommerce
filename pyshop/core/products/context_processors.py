from .models import Cart, Wishlist

def global_counts(request):
    if request.user.is_authenticated:
        cart = Cart.objects.filter(user=request.user).first()
        cart_count = cart.items.count() if cart else 0

        wishlist_count = Wishlist.objects.filter(user=request.user).count()
    else:
        cart_count = 0
        wishlist_count = 0

    return {
        'cart_count': cart_count,
        'wishlist_count': wishlist_count
    }