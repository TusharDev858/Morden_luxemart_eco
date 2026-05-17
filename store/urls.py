from django.urls import path
from . import views

app_name = 'store'

urlpatterns = [
    path('', views.home, name='home'),
    path('products/', views.ProductListView.as_view(), name='product_list'),
    path('products/<slug:slug>/', views.product_detail, name='product_detail'),
    path('category/<slug:slug>/', views.ProductListView.as_view(), name='category'),
    path('search/', views.search, name='search'),
    path('validate-coupon/', views.validate_coupon, name='validate_coupon'),
]
