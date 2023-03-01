from django.shortcuts import render
from django.http import JsonResponse
from .models import *


# Create your views here.
def store(request):
    products = Product.objects.all()
    
    context = {
        'products':products
    }
    return render(request, 'store/store.html', context)

def cart(request):
    #first check authenticated user
    if request.user.is_authenticated:
        customer = request.user.customer #access the customer account of user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)#get order if it exists or create it must be for thr customer and only orders that are false on complete
        items = order.orderitem_set.all() #get items attached to the order
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}#these are manually set so that we have defaults incase totals are not set

    context = {
        'items' : items,
        'order':order
    }
    return render(request, 'store/cart.html', context)

def checkout(request):
    #we want to repeat what we have done in the cart method so we can have access to cart detail to show in the checkout summary
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
    else:
        #Create Empty cacrt for now for non-logged in users
        order = {'get_cart_total':0, 'get_cart_items':0}
        items = []

    context = {
        'items':items,
        'order':order
    }
    return render(request, 'store/checkout.html', context)

def updateItem(request):
    return JsonResponse('Item was added', safe=False)
    