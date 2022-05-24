from django.urls import path
from .views import Cart
from .views import Index, Productlist, Buy, Register, Login
from .views import OrderView
from django.contrib.auth.middleware import AuthenticationMiddleware
from . import views


urlpatterns = [
    path('', Index.as_view(), name = 'home'),
    path('register/', Register.as_view(), name='register'),
    path('login/', Login.as_view(), name='login'),
    path('logout/', views.logout, name='logout'),
    path('cart/', Cart.as_view(), name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('buy/', Buy.as_view(), name='buy'),
    path('orders/', AuthenticationMiddleware(OrderView.as_view()), name='orders'),
    path('contact/', views.contact, name='contact'),
    path('myaccount/', views.myaccount, name='myaccount'),
    path('productdetail/', views.productdetail, name='productdetail'),
    path('productlist/',Productlist.as_view(), name='productlist'),
    path('wishlist/', views.wishlist, name='wishlist'),
]
