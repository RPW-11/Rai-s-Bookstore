from django.contrib import admin
from .models import Book, Customer, Order, OrderItem, ShippingAddress
# Register your models here.
admin.site.register(Book)
admin.site.register(Customer)
admin.site.register(Order)
admin.site.register(OrderItem)
admin.site.register(ShippingAddress)