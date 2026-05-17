from django.urls import path
from . import views

app_name = 'wishlist'

urlpatterns = [
    path('', views.wishlist, name='list'),
    path('toggle/<uuid:product_id>/', views.toggle_wishlist, name='toggle'),
]
