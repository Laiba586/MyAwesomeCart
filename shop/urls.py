from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path('',views.index,name = 'shop home'),
    path('about',views.about,name = 'About us'),
    path('contact',views.contact,name = 'contact'),
    path('search',views.search,name = 'search'),
    path('catagories',views.catagories,name = 'catagories'),
    path("products/<int:myid>", views.productView, name="productView"),
    path('tracker',views.tracker,name = 'trackingstatus'),
    path('checkout',views.checkout,name = 'checkout')

]
