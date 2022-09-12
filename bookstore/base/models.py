from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Book(models.Model):
    title = models.CharField(null=False, max_length=200)
    author = models.CharField(null=False, max_length=200)
    publisher = models.CharField(null=False, max_length=200)
    isbn = models.CharField(null=False, max_length=200)
    itemWeight = models.PositiveIntegerField(null=False)
    dimension = models.CharField(max_length=10)
    pages = models.PositiveIntegerField(null=False)
    language = models.CharField(null=False, max_length=200)
    ratings = models.PositiveIntegerField(null=True, blank=True)
    price = models.DecimalField(null=False, decimal_places=2, max_digits=10)
    description = models.TextField(null=True, blank=True)
    image = models.ImageField(null=True)
    quantity = models.PositiveIntegerField(default=0)
    created = models.DateTimeField(auto_now_add=True)
    class Meta:
        ordering = ['-created']
    

    def __str__(self):
        return self.title


class Customer(models.Model):
    user = models.OneToOneField(User, null=True, blank=True, on_delete=models.CASCADE)
    name = models.CharField(max_length=225, null=True)
    phone_number = models.CharField(max_length=225, null=True)
    email = models.EmailField(max_length=225, null=False)
    profile_pic = models.ImageField(null=True)
    date_created = models.DateTimeField(auto_now_add=True, null=True)


    def __str__(self):
        return self.name


class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    date_ordered = models.DateTimeField(auto_now_add=True)
    complete = models.BooleanField(default=False, null=True, blank=False)
    transaction_id = models.CharField(max_length=225, null=True)


    def __str__(self):
        return str(self.id)

    @property
    def get_total_price(self):
        items = self.orderitem_set.all()
        total = sum([item.get_total_price for item in items])
        return total

    @property
    def get_total_items(self):
        items = self.orderitem_set.all()
        total_items = sum([item.quantity for item in items])
        return total_items


class OrderItem(models.Model):
    book = models.ForeignKey(Book, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.PositiveIntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    @property
    def get_total_price(self):
        return self.quantity * self.book.price


class ShippingAddress(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    address = models.CharField(max_length=225, null=True)
    city = models.CharField(max_length=225, null=True)
    state = models.CharField(max_length=225, null=True)
    zipcode = models.CharField(max_length=225, null=True)
    date_added = models.CharField(max_length=225, null=True)


    def __str__(self):
        return self.address



