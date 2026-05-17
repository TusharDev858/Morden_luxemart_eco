from django.urls import path
from . import views

app_name = 'orders'

urlpatterns = [
    path('checkout/', views.checkout, name='checkout'),
    path('create-payment-intent/', views.create_stripe_payment_intent, name='create_payment_intent'),
    path('place-order/', views.place_order, name='place_order'),
    path('my-orders/', views.order_list, name='order_list'),
    path('<uuid:pk>/', views.order_detail, name='order_detail'),
    path('track/', views.order_tracking, name='tracking'),
]
