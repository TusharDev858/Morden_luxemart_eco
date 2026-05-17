"""
LuxeMart URL Configuration
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from django.contrib.sitemaps.views import sitemap

admin.site.site_header = "LuxeMart Administration"
admin.site.site_title = "LuxeMart Admin"
admin.site.index_title = "Welcome to LuxeMart Admin Panel"

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('store.urls', namespace='store')),
    path('users/', include('users.urls', namespace='users')),
    path('orders/', include('orders.urls', namespace='orders')),
    path('cart/', include('cart.urls', namespace='cart')),
    path('wishlist/', include('wishlist.urls', namespace='wishlist')),
    path('reviews/', include('reviews.urls', namespace='reviews')),
    path('contact/', include('contact.urls', namespace='contact')),
]

if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
