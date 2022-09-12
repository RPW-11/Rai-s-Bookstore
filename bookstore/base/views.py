from django.shortcuts import redirect, render
from django.contrib.auth.models import User
from django.contrib import messages
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import UserCreationForm
from django.http import JsonResponse
from .models import *
from .forms import BookForm
import json

# Create your views here.

def home(request):
    # if the user is logged in
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer)
        itemsCount = order.get_total_items
    else:
        itemsCount = 0

    books = Book.objects.all().order_by('title')
    for book in books:
        if book.ratings == 0:
            book.ratings = None
        else:
            book.ratings = range(book.ratings)
    context = {'books':books, 'itemsCount':itemsCount}
    return render(request, 'base/home.html', context)

@login_required(login_url='/login')
def book_profile(request, pk):
    book = Book.objects.get(id=pk)
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer)
    itemsCount = order.get_total_items
    context = {'book':book,'itemsCount':itemsCount}
    return render (request, 'base/book_profile.html', context)

@login_required(login_url='/login')
def sell_book(request):
    form = BookForm()
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer)
    itemsCount = order.get_total_items
    context = {'form':form, 'itemsCount':itemsCount}
    return render(request, 'base/sell_book.html', context)


def login_page(request):
    if request.method == 'POST':
        username = request.POST.get('username').lower()
        password = request.POST.get('password')
        try:
            user = User.objects.get(username=username)
        except:
            messages.error(request, "User doesn't exist")
        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "Wrong username or password, please try again")
        
    context = {}
    return render (request, 'base/login_register.html', context)


def register_user(request):
    page = 'register'
    register_form = UserCreationForm()

    # when the form is filled
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.username = user.username.lower()
            user.save()
            login(request, user)
            return redirect('home')
        else:
            messages.error(request, "An error has occured")
    context = {'page':page, 'form':register_form}
    return render(request, 'base/login_register.html', context)


def logout_page(request):
    logout(request)
    return redirect ('home')

@login_required(login_url='/login')
def user_profile(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer=customer)
    itemsCount = order.get_total_items
    context = {'itemsCount':itemsCount}
    return render(request, 'base/user_profile.html', context)

@login_required(login_url='/login')
def cart(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    items = order.orderitem_set.all()
    itemsCount = order.get_total_items
    context = {'items':items, 'order':order, 'itemsCount':itemsCount}
    return render (request, 'base/cart.html', context)

@login_required(login_url='/login')
def checkout(request):
    customer = request.user.customer
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    items = order.orderitem_set.all()
    itemsCount = order.get_total_items
    context = {'items':items, 'order':order, 'itemsCount':itemsCount}
    return render(request, 'base/checkout.html', context)

@login_required(login_url='/login')
def updateItem(request):
    data = json.loads(request.body)
    bookId = data['bookId']
    action = data['action']
    
    customer = request.user.customer
    book = Book.objects.get(id=bookId)
    order, created = Order.objects.get_or_create(customer = customer, complete = False)
    orderItem, created = OrderItem.objects.get_or_create(order=order, book=book)

    if action == 'add':
        orderItem.quantity += 1
    elif action == 'remove':
        orderItem.quantity -= 1
    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('item was added', safe=False)

 