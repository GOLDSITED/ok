from django.urls import path
from cart.views import add_to_cart, remove_from_cart, CartView, decreaseCart
from . views import home, ProductDetail, Home
app_name= 'products'

urlpatterns = [
    # path('', Home.as_view(), name='home'),
    path('', home, name='home'),
    path('p', Home.as_view(), name='home'),
    path('product/<int:slug>/', ProductDetail.as_view(), name='product'),
    path('cart/', CartView, name='cart-home'),
    path('cart/<int:slug>', add_to_cart, name='cart'),
    path('decrease-cart/<int:slug>', decreaseCart, name='decrease-cart'),
    path('remove/<int:slug>', remove_from_cart, name='remove-cart'),
]