from django.urls import path
from . import views

urlpatterns = [
    path('pay/', views.payment, name='payment'),
    path('payment_response/', views.payment_response, name='payment_response'),
    
]