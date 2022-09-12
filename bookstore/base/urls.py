from unicodedata import name
from . import views
from django.urls import path
# app urls
urlpatterns = [
    path('', views.home, name='home'),
    path('profile/<str:pk>/', views.book_profile, name='book-profile'),
    path('sell/', views.sell_book, name='sell-book'),
    path('login/',views.login_page, name='login'),
    path('logout/', views.logout_page, name='logout'),
    path('register/', views.register_user, name='register'),
    path('user-profile', views.user_profile, name='user-profile'),
    path('cart/', views.cart, name='cart'),
    path('checkout/', views.checkout, name='checkout'),
    path('update-item', views.updateItem, name='update-item'),
]