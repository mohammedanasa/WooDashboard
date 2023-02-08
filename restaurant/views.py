from django.shortcuts import render, redirect,get_object_or_404
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.views.generic.list import ListView
from restaurant.forms import *
import requests
import base64
import json
from woocommerce import API


#----------------------------------------RESTAURANT--------------------------------------#

#List all the restaurants
def restaurant_list(request):
    webhook_url = "https://woorest.cognigence.in/wp-json/deliverect/busymode"
    headers = {
                "Content-Type":"application/json"
            }

    if request.method == 'POST':
        restaurant_id = request.POST.get('restaurant_id')
        restaurant = Restaurant.objects.get(lid=restaurant_id)
        if request.POST.get('action') == 'Close':
            restaurant.status = Restaurant.CLOSED
            data = {
                "accountId": "1234",
                "locationId": "5678",
                "status": "ONLINE"
            }

        # Send the POST request with the data to the webhook endpoint
            response = requests.post(webhook_url, headers= headers, json=data)
            print(response)

        else:
            restaurant.status = Restaurant.OPEN
            data = {
                "accountId": "1234",
                "locationId": "5678",
                "status": "PAUSED"
            }

        # Send the POST request with the data to the webhook endpoint
            response = requests.post(webhook_url, headers= headers, json=data)
            print(response)
        restaurant.save()
        return redirect('restaurant:locations')

    restaurants = Restaurant.objects.filter(owner=request.user)
    return render(request, 'restaurant/location/locations.html', {'restaurants': restaurants})

#----------------------------------------Product Views------------------------------------------#
#Product Views

@login_required
def create_or_update_product(request, pid=None):
    product = get_object_or_404(Product, pid=pid) if pid else None
    modifier_groups = ModifierGroup.objects.filter(products=product) if product else []

    if request.method == 'POST':
        form = ProductForm(request.POST,request.FILES, instance=product)
        if form.is_valid():
            product = form.save(commit=False)
            product.owner = request.user
            category = form.cleaned_data.get('category')
            product.catprods.set(form.cleaned_data.get('category'))
            product.save()
            messages.success(request, 'Product has been successfully saved')
            return redirect('restaurant:update-product',pid=product.pid)

    else:
        form = ProductForm(instance=product)
    return render(request, 'restaurant/product/product.html', {'form': form,'product':product,'modifier_groups':modifier_groups})

class ProductList(LoginRequiredMixin,ListView):
    model = Product
    context_object_name = 'products'
    template_name = 'restaurant/product/products.html'


    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        return context



@login_required
def delete_product(request, pid):
    product = get_object_or_404(Product, pid=pid)
    if request.method == 'POST':
        product.delete()
        messages.success(request, 'product has been successfully deleted')

        return redirect('restaurant:products')
    return render(request, 'restaurant/product/delete-product.html', {'product': product})



#----------------------------------------Category Views-----------------------------------------#

#Category Views
@login_required
def create_or_update_category(request, cid=None):
    category = get_object_or_404(Category, cid=cid) if cid else None
    products = Product.objects.filter(catprods=category) if category else []
    if request.method == 'POST':
        form = CategoryForm(request.POST,request.FILES, instance=category)
        if form.is_valid():
            category = form.save(commit=False)
            category.owner = request.user
            category.save()
            messages.success(request, 'Category has been successfully saved')
            return redirect('restaurant:update-category',cid=category.cid)
    else:
        form = CategoryForm(instance=category)
    return render(request, 'restaurant/category/category.html', {'form': form, 'category':category, 'products':products})

class CategoryList(LoginRequiredMixin,ListView):
    model = Category
    context_object_name = 'categories'
    template_name = 'restaurant/category/categories.html'

    def get_queryset(self):
        return Category.objects.filter(owner=self.request.user) 

@login_required
def delete_category(request, cid):
    category = get_object_or_404(Category, cid=cid)
    if request.method == 'POST':
        category.delete()
        messages.success(request, 'Category has been successfully deleted')

        return redirect('restaurant:categories')
    return render(request, 'restaurant/category/delete-category.html', {'category': category})




#------------------------------------------- TESTING --------------------------------------------#


#WooCommerce Test - SUCCESS
def fetch_products(request):

    '''# Make a GET request to the WooCommerce API to retrieve a list of products
    url = 'https://wa.biancouk.com/wp-json/wc/v3/products'
    # API credentials
    consumer_key = "ck_aca584ab9f02508a1ecfefe9020f7fa83e1ad079".encode("utf-8")
    consumer_secret = "cs_147ff37c0c4b41dae34d7cb749bd4d3af73dce69".encode("utf-8")'''

    '''# Make a GET request to the WooCommerce API to retrieve a list of products
    url = 'https://woorest.cognigence.in/wp-json/wc/v3/products'

    # API credentials
    consumer_key = "ck_325975577d69b78d389c8ed95ab73846611cf12a".encode("utf-8")
    consumer_secret = "cs_c2c68fe5f1cf8b4bbe197c146b880a44b455c666".encode("utf-8")

    
    # API request headers
    headers = {
        "Authorization": "Basic " + base64.b64encode(consumer_key + b":" + consumer_secret).decode("utf-8"),
        "User-Agent": "MyApp/1.0",
        "Accept": "application/json",
        "Content-Type": "application/json"
    }
    '''

    wcapi = API(
        url = 'https://woorest.cognigence.in',

        # API credentials
        consumer_key = "ck_325975577d69b78d389c8ed95ab73846611cf12a",
        consumer_secret = "cs_c2c68fe5f1cf8b4bbe197c146b880a44b455c666",
        version = "wc/v3"

    )

    response = wcapi.get("products", params={'per_page': 100})
    products = response.json()

    # Check if the request was successful
    if response.status_code == 200:
        # Display the product data
        products = response.json()
        for product_data in products:
            name = product_data.get("name")
            description = product_data.get("description")
            price = product_data.get("price")

            product = Product(name=name, description=description, price=price, owner = request.user)
            product.save()
        print(len(products))

    else:
        # Display an error message
        print("Failed to retrieve product data. Response code:", response.status_code)
        
    # Render the list of products in a template
    return render(request, 'restaurant/wootest.html', {'products': products})


#Working except the while part
def fetch_product_test(request):
    #url = 'https://woorest.cognigence.in/wp-json/wc/v3/products'

    # API credentials
    #consumer_key = "ck_325975577d69b78d389c8ed95ab73846611cf12a".encode("utf-8")
    #consumer_secret = "cs_c2c68fe5f1cf8b4bbe197c146b880a44b455c666".encode("utf-8")

    wcapi = API(
        url = 'https://woorest.cognigence.in',
        consumer_key = "ck_325975577d69b78d389c8ed95ab73846611cf12a",
        consumer_secret = "cs_c2c68fe5f1cf8b4bbe197c146b880a44b455c666",
        version = "wc/v3"
    )

    response = wcapi.get("products", params={'per_page': 100}).json()
    print(len(response))

    '''page = 0
    while True:
        response = wcapi.get("products", params={'per_page': 100, 'page': page}).json()
        # retrieve ids from **products**
        if len(response) == 0: # no more products
            break
        page = page + 1

    print(response)'''
    


def create_woocommerce_product_individually():
    data = {
            "name": name,
            "sku": fetched_sku,
            "images": [
                    {
                    "src": fetched_url
                    },
                      ],
            "short_description": short_description,
            "description": description,
            "categories": [
            {
                "id": woo_commerce_category_id
            }
                        ],
            }
    #post data to the woocommerce API
    wcapi.post("products",data).json()
    print(" 3A STEP - WOO PRODUCT CREATED IN THE SITE")


