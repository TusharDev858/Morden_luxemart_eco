"""
Cart Views - Add, remove, update cart items
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.contrib import messages
import json

from .models import Cart, CartItem
from store.models import Product, ProductVariant


def get_or_create_cart(request):
    """Get or create cart for current user/session"""
    if request.user.is_authenticated:
        cart, _ = Cart.objects.get_or_create(user=request.user)
        # Merge session cart if exists
        if request.session.session_key:
            try:
                session_cart = Cart.objects.get(session_key=request.session.session_key)
                for item in session_cart.items.all():
                    existing = cart.items.filter(product=item.product, variant=item.variant).first()
                    if existing:
                        existing.quantity += item.quantity
                        existing.save()
                    else:
                        item.cart = cart
                        item.save()
                session_cart.delete()
            except Cart.DoesNotExist:
                pass
    else:
        if not request.session.session_key:
            request.session.create()
        cart, _ = Cart.objects.get_or_create(session_key=request.session.session_key)
    return cart


def cart_detail(request):
    """Cart page"""
    cart = get_or_create_cart(request)
    return render(request, 'cart/cart.html', {'cart': cart})


@require_POST
def add_to_cart(request, product_id):
    """Add product to cart"""
    product = get_object_or_404(Product, pk=product_id, is_active=True)
    cart = get_or_create_cart(request)
    quantity = int(request.POST.get('quantity', 1))
    variant_id = request.POST.get('variant_id')

    variant = None
    if variant_id:
        variant = get_object_or_404(ProductVariant, pk=variant_id, product=product)

    item, created = CartItem.objects.get_or_create(
        cart=cart, product=product, variant=variant
    )
    if created:
        item.quantity = quantity
    else:
        item.quantity += quantity
    item.save()

    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'message': f'{product.name} added to cart!',
            'cart_count': cart.total_items,
        })
    messages.success(request, f'{product.name} added to cart!')
    return redirect('cart:detail')


@require_POST
def update_cart(request, item_id):
    """Update cart item quantity"""
    item = get_object_or_404(CartItem, pk=item_id)
    quantity = int(request.POST.get('quantity', 1))
    if quantity <= 0:
        item.delete()
    else:
        item.quantity = quantity
        item.save()
    cart = item.cart
    return JsonResponse({
        'success': True,
        'item_total': str(item.total_price) if quantity > 0 else '0',
        'cart_total': str(cart.total),
        'cart_count': cart.total_items,
    })


def remove_from_cart(request, item_id):
    """Remove item from cart"""
    item = get_object_or_404(CartItem, pk=item_id)
    cart = item.cart
    item.delete()
    if request.headers.get('X-Requested-With') == 'XMLHttpRequest':
        return JsonResponse({
            'success': True,
            'cart_count': cart.total_items,
            'cart_total': str(cart.total),
        })
    messages.success(request, 'Item removed from cart.')
    return redirect('cart:detail')
