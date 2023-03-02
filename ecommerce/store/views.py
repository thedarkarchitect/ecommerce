from django.shortcuts import render
from django.http import JsonResponse
from .models import *
import json
import datetime
from django.views.decorators.csrf import csrf_exempt

# Create your views here.
def store(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items#shows cart items
    else:
        #Create Empty cacrt for now for non-logged in users
        order = {'get_cart_total':0, 'get_cart_items':0}
        items = []
        cartItems == order['get_cart_items']#this will show guest users their  cart items also


    products = Product.objects.all()
    
    context = {
        'products':products,
        'cartItems':cartItems
    }
    return render(request, 'store/store.html', context)


def cart(request):
    #first check authenticated user
    if request.user.is_authenticated:
        customer = request.user.customer #access the customer account of user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)#get order if it exists or create it must be for thr customer and only orders that are false on complete
        items = order.orderitem_set.all() #get items attached to the order
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total': 0, 'get_cart_items': 0}#these are manually set so that we have defaults incase totals are not set
        cartItems == order['get_cart_items']

    context = {
        'items' : items,
        'order':order,
        'cartItems':cartItems
    }
    return render(request, 'store/cart.html', context)


def checkout(request):
    #we want to repeat what we have done in the cart method so we can have access to cart detail to show in the checkout summary
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()#query all items 
        cartItems = order.get_cart_items
    else:
        #Create Empty cacrt for now for non-logged in users
        order = {'get_cart_total':0, 'get_cart_items':0, 'shipping':False}
        items = []
        cartItems == order['get_cart_items']

    context = {
        'items':items,
        'order':order,
        'cartItems': cartItems
    }
    return render(request, 'store/checkout.html', context)


def updateItem(request):
    data = json.loads(request.body)#this give you data to the response created in the cart js and it will come as a dictionary
    productId = data['productId']
    action = data['action']
    print('Action: ', action)
    print('Product: ', productId)

    customer = request.user.customer #query the loged in customer
    product = Product.objects.get(id=productId) #query product with reference to the productId
    order, created = Order.objects.get_or_create(customer=customer, complete=False)#this get or creates an order attached to the logged in customer

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)#we want to be able to add or subtract the order items throught the website if the product and order exist

    if action == 'add':
        orderItem.quantity = (orderItem.quantity + 1) #this adds to a particular product selected by user in cart if the want the items is large quantities helps the website to do the tallies
    elif action == 'remove':
        orderItem.quantity = (orderItem.quantity - 1)

    orderItem.save()

    #remove order if the quantity is below zero
    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)#return this to the template whenever a function is called 

@csrf_exempt
def processOrder(request):
    transaction_id = datetime.datetime.now().timestamp()
    data = json.loads(request.body)

    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        total = float(data['form']['total'])
        order.transaction_id = transaction_id

        #user will not be able to manipulate total, this make sure cart total matches the paypal total
        if total == order.get_cart_total:
            order.complete = True
        order.save()

        if order.shipping == True:
            ShippingAddress.objects.create(#this will set the values of the shipping attributes
                customer=customer,
                order=order,
                address=data['shipping']['address'],#this is from the js side
                city=data['shipping']['city'],
                state=data['shipping']['state'],
                zipcode=data['shipping']['zipcode']
            )
    else:
        print('User is not logged in..')

    return JsonResponse('Payment submitted..', safe=False)#this work after payment made