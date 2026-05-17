from django.shortcuts import render, get_object_or_404, redirect
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.contrib import messages

from .models import WishlistItem
from store.models import Product


@login_required
def wishlist(request):
    items = WishlistItem.objects.filter(user=request.user).select_related('product').order_by('-added_at')
    return render(request, 'wishlist/wishlist.html', {'items': items})


@login_required
def toggle_wishlist(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    item, created = WishlistItem.objects.get_or_create(user=request.user, product=product)
    if not created:
        item.delete()
        added = False
        message = f'{product.name} removed from wishlist'
    else:
        added = True
        message = f'{product.name} added to wishlist!'

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'added': added,
            'message': message,
            'count': request.user.wishlist_items.count()
        })
    messages.success(request, message)
    return redirect(request.META.get('HTTP_REFERER', 'wishlist:list'))
