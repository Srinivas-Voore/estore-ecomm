from django.contrib.auth.hashers import make_password, check_password
from django.http import HttpResponseRedirect
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
# Create your views here.
from django.views import View
from .models import Product
from .models import Customer
from .models import Order
from .models import Category


def index(request):
    products = None
    # print(products)
    # return render(request, 'orders/order.html')
    categories = Category.get_all_categories()
    categoryID = request.GET.get('category')
    if categoryID:
        products = Product.get_all_products_by_categoryid(categoryID)
    else:
        products = Product.get_all_products
    data = {}
    data['products'] = products
    data['categories'] = categories
    return render(request, 'home/index.html', data)


class Index(View):

    def post(self, request):

        remove = request.POST.get('remove')
        product = request.POST.get('product')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print("kkkkkkkk:",request.session['cart'])
        return redirect('home')

    def get(self, request):
        products = None
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        #request.session.get('cart').clear()
        # print(products)
        # return render(request, 'orders/order.html')
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products
        data = {}
        data['products'] = products
        data['categories'] = categories
        return render(request, 'home/index.html', data)


class Register(View):

    def get(self, request):
        return render(request, 'home/login.html')
    def post(self, request):
        postData = request.POST
        first_name = postData.get('firstname')
        last_name = postData.get('lastname')
        phone = postData.get('phone')
        email = postData.get('email')
        password = postData.get('password')

        # validation

        value = {
            'first_name': first_name,
            'last_name': last_name,
            'phone': phone,
            'email': email
        }

        error_message = None

        customer = Customer(first_name=first_name, last_name=last_name, phone=phone, email=email, password=password)

        if not first_name:
            error_message = "First name required"

        elif first_name:
            if len(first_name) < 4:
                error_message = "First name must be 4 characters long"

        if not last_name:
            error_message = "Last name required"

        if last_name:
            if len(last_name) < 4:
                error_message = "Last name must be 4 characters long"

        if not phone:
            error_message = 'Phone Number required'

        if len(phone) < 10:
            error_message = 'Phone Number must be not less than 10 char Long'

        if len(phone) > 10:
            error_message = 'Phone Number must be not more than 10 char Long'

        if len(password) < 6:
            error_message = 'Password must be 6 char long'

        if len(email) < 5:
            error_message = 'Email must be 5 char long'

        if customer.isExists():
            error_message = "Email Address already registred"

        # saving
        if not error_message:
            print(first_name, last_name, phone, email, password)
            customer.password = make_password(customer.password)
            customer.register()
            return redirect('home')
        else:
            data = {
                'error': error_message,
                'values': value
            }
            return render(request, 'home/login.html', data)


class Login(View):

    return_url = None
    def get(self, request):
        Login.return_url = request.GET.get('return_url')
        return render(request , 'home/login.html')

    def post(self, request):
        email = request.POST.get('email')
        password = request.POST.get('password')
        customer = Customer.get_customer_by_email(email)
        error_message = None
        if customer:
            flag = check_password(password, customer.password)
            if flag:
                request.session['customer'] = customer.id

                if Login.return_url:
                    return HttpResponseRedirect(Login.return_url)

                else:
                    Login.return_url = None
                    return redirect('home')

            else:
                error_message = 'Email or Password invalid !!'
        else:
            error_message = 'Email or Password invalid !!'

        print(email, password)
        return render(request, 'home/login.html', {'error': error_message})


def logout(request):
    request.session.clear()
    return redirect('login')


class Cart(View):
    def get(self , request):
        ids = list(request.session.get('cart').keys())
        products = Product.get_products_by_id(ids)
        print(products)
        return render(request , 'home/cart.html' , {'products' : products} )


def checkout(request):
    return render(request, 'home/checkout.html')


class Buy(View):
    def post(self, request):
        address = request.POST.get('address')
        phone = request.POST.get('phone')
        customer = request.session.get('customer')
        cart = request.session.get('cart')
        products = Product.get_products_by_id(list(cart.keys()))
        print(address, phone, customer, cart, products)

        for product in products:
            print(cart.get(str(product.id)))
            order = Order(customer=Customer(id=customer),
                          product=product,
                          price=product.price,
                          address=address,
                          phone=phone,
                          quantity=cart.get(str(product.id)))
            order.save()
        request.session['cart'] = {}

        return redirect('cart')


class OrderView(View):
    def get(self , request ):
        customer = request.session.get('customer')
        orders = Order.get_orders_by_customer(customer)
        print(orders)
        return render(request, 'home/orders.html', {'orders': orders})


def contact(request):
    return render(request, 'home/contact.html')


def myaccount(request):
    return render(request, 'home/my-account.html')


def productdetail(request):
    return render(request, 'home/product-detail.html')


class Productlist(View):

    def post(self, request):

        remove = request.POST.get('remove')
        product = request.POST.get('product')
        cart = request.session.get('cart')
        if cart:
            quantity = cart.get(product)
            if quantity:
                if remove:
                    if quantity <= 1:
                        cart.pop(product)
                    else:
                        cart[product] = quantity - 1
                else:
                    cart[product] = quantity + 1

            else:
                cart[product] = 1
        else:
            cart = {}
            cart[product] = 1

        request.session['cart'] = cart
        print("kkkkkkkk:",request.session['cart'])
        return redirect('productlist')

    def get(self, request):
        products = None
        cart = request.session.get('cart')
        if not cart:
            request.session['cart'] = {}
        #request.session.get('cart').clear()
        # print(products)
        # return render(request, 'orders/order.html')
        categories = Category.get_all_categories()
        categoryID = request.GET.get('category')
        if categoryID:
            products = Product.get_all_products_by_categoryid(categoryID)
        else:
            products = Product.get_all_products
        data = {}
        data['products'] = products
        data['categories'] = categories
        return render(request, 'home/product-list.html', data)


def wishlist(request):
    return render(request, 'home/wishlist.html')