from django.urls import path
from . import views

urlpatterns = [
    path('', views.product_list, name='product_list'),
    path('product/<int:id>/', views.product_detail, name='product_detail'),

    path('cart/', views.cart_view, name='cart'),

    path('add-to-cart/<int:id>/', views.add_to_cart, name='add_to_cart'),
    path('remove/<int:id>/', views.remove_from_cart, name='remove_from_cart'),
    path('wishlist/', views.wishlist_view, name='wishlist'),
    path('wishlist/add/<int:id>/', views.add_to_wishlist, name='add_to_wishlist'),
    path('wishlist/remove/<int:id>/', views.remove_from_wishlist, name='remove_from_wishlist'),
    path('increase/<int:id>/', views.increase_quantity, name='increase_quantity'),
    path('decrease/<int:id>/', views.decrease_quantity, name='decrease_quantity'),

    path('checkout/', views.checkout, name='checkout'),
    path('orders/', views.order_history, name='order_history'),
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    path('payment-success/', views.payment_success, name='payment_success'),
    path('verify-payment/', views.verify_payment, name='verify_payment'),
    path('track-order/<int:order_id>/', views.track_order, name='track_order'),
    path('invoice/<int:order_id>/', views.download_invoice, name='download_invoice'),
    path(
    'add-review/<int:product_id>/',
    views.add_review,
    name='add_review'
),
]