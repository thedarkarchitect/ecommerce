from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Customer(models.Model):
    user = models.OneToOneField(User, null=True, on_delete=models.CASCADE)#one user makes one customer account everytime
    name= models.CharField(max_length=200, null=True)
    email = models.CharField(max_length=200)

    def __str__(self) -> str:
        return self.name
    
class Product(models.Model):
    name = models.CharField(max_length=200)
    price = models.DecimalField(max_digits=7, decimal_places=2)
    digital = models.BooleanField(default=False, null=True, blank=True)#by default all items are physciall itemss
    image = models.ImageField(null=True, blank=True)

    def __str__(self) -> str:
        return self.name
    
    @property #this is going to allow us to access the method below as an attribute of the model
    def imageURL(self):
        try:
            url = self.image.url
        except:
            url = ''
        return url
    
class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True)#one customer makes many orders so this is a one to Many relationship 
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=100, null=True)

    def __str__(self)->str:
        return str(self.id)
    
    #we shall use the @property decorator to make those methods attributes of this model
    #to get the cart items and total price of items in cart 
    @property
    def shipping(self):
        shipping = False #shipping starts off as false so no shipping
        orderitems = self.orderitem_set.all()#query all order items
        for i in orderitems:
            if i.product.digital == False: #checking if the product is physicall meaning it needs shipping
                shipping = True #then if it is a physicall product it will be allowed to ship
        return shipping
    
    @property
    def get_cart_total(self):#this returns the total of all the items in the cart
        orderitems = self.orderitem_set.all()#this gives you access to all the orderitems in your models
        total = sum([item.get_total for item in orderitems])#get total is got from orderitems model that why we set it first so we can use it here
        return total
    
    @property
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()#this gives you access to all the orderitems in your models
        total = sum([item.quantity for item in orderitems]) #this sums up items and returns a total we are going to use in the cart to shoe total items
        return total
    
class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    #we need to get total price of ordered items and total price
    #we shall use the @property decorator to make those methods attributes of this model 
    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, null=True)
    address = models.CharField(max_length=200, null=False)
    city = models.CharField(max_length=200, null=False)
    state = models.CharField(max_length=200, null=False)
    zipcode = models.CharField(max_length=200, null=False)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self) -> str:
        return self.address