"""
Orders Views - Checkout, Stripe, PayPal, Place Order, Tracking
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
import json, stripe

from .models import Order, OrderItem
from cart.views import get_or_create_cart

stripe.api_key = settings.STRIPE_SECRET_KEY


def _calculate_totals(cart):
    subtotal = float(cart.subtotal)
    shipping = 0.0 if subtotal >= 75 else 9.99
    tax = round(subtotal * 0.08, 2)
    discount = float(cart.coupon_discount)
    total = round(subtotal + shipping + tax - discount, 2)
    return subtotal, shipping, tax, discount, total


def checkout(request):
    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')

    addresses = []
    if request.user.is_authenticated:
        addresses = request.user.addresses.filter(address_type='shipping')

    subtotal, shipping, tax, discount, total = _calculate_totals(cart)
    return render(request, 'orders/checkout.html', {
        'cart': cart, 'addresses': addresses,
        'subtotal': subtotal, 'shipping': shipping,
        'tax': tax, 'total': total,
        'stripe_public_key': settings.STRIPE_PUBLIC_KEY,
        'paypal_client_id': settings.PAYPAL_CLIENT_ID,
    })


def create_stripe_payment_intent(request):
    if request.method == 'POST':
        try:
            cart = get_or_create_cart(request)
            _, _, _, _, total = _calculate_totals(cart)
            intent = stripe.PaymentIntent.create(
                amount=int(total * 100),
                currency='usd',
                metadata={'cart_id': str(cart.id)},
            )
            return JsonResponse({'client_secret': intent.client_secret})
        except stripe.error.StripeError as e:
            return JsonResponse({'error': str(e)}, status=400)
        except Exception as e:
            return JsonResponse({'error': 'An error occurred. Please try again.'}, status=500)
    return JsonResponse({'error': 'Invalid request'}, status=400)


def place_order(request):
    if request.method != 'POST':
        return redirect('orders:checkout')

    cart = get_or_create_cart(request)
    if not cart.items.exists():
        messages.warning(request, 'Your cart is empty.')
        return redirect('cart:detail')

    data = request.POST
    subtotal, shipping_cost, tax, discount, total = _calculate_totals(cart)
    payment_method = data.get('payment_method', 'stripe')
    payment_intent_id = data.get('payment_intent_id', '')
    is_paid = bool(payment_intent_id) or payment_method == 'paypal'

    order = Order.objects.create(
        user=request.user if request.user.is_authenticated else None,
        shipping_name=data.get('full_name', ''),
        shipping_email=data.get('email', ''),
        shipping_phone=data.get('phone', ''),
        shipping_address=data.get('address', ''),
        shipping_city=data.get('city', ''),
        shipping_state=data.get('state', ''),
        shipping_postal=data.get('postal_code', ''),
        shipping_country=data.get('country', 'United States'),
        subtotal=subtotal,
        shipping_cost=shipping_cost,
        tax_amount=tax,
        discount_amount=discount,
        total_price=total,
        payment_method=payment_method,
        stripe_payment_intent=payment_intent_id,
        coupon_code=cart.coupon_code,
        status='confirmed' if is_paid else 'pending',
        payment_status='paid' if is_paid else 'unpaid',
    )

    for item in cart.items.all():
        image_url = ''
        try:
            img = item.product.main_image
            if img:
                image_url = request.build_absolute_uri(img.url)
        except Exception:
            pass
        OrderItem.objects.create(
            order=order,
            product=item.product,
            product_name=item.product.name,
            product_image=image_url,
            variant_info=str(item.variant) if item.variant else '',
            quantity=item.quantity,
            unit_price=item.unit_price,
        )
        # Decrease stock
        p = item.product
        p.stock_quantity = max(0, p.stock_quantity - item.quantity)
        p.save(update_fields=['stock_quantity', 'stock_status'])

    cart.items.all().delete()
    cart.coupon_code = ''
    cart.coupon_discount = 0
    cart.save(update_fields=['coupon_code', 'coupon_discount'])

    messages.success(request, f'🎉 Order #{order.order_number} placed successfully! Thank you for shopping with us.')
    return redirect('orders:order_detail', pk=order.pk)


def order_list(request):
    if not request.user.is_authenticated:
        return redirect('users:login')
    orders = Order.objects.filter(user=request.user).prefetch_related('items').order_by('-created_at')
    return render(request, 'orders/order_list.html', {'orders': orders})


def order_detail(request, pk):
    if request.user.is_authenticated:
        order = get_object_or_404(Order, pk=pk, user=request.user)
    else:
        order = get_object_or_404(Order, pk=pk)
    return render(request, 'orders/order_detail.html', {'order': order})


def order_tracking(request):
    order = None
    if request.method == 'POST':
        order_number = request.POST.get('order_number', '').strip().upper()
        email = request.POST.get('email', '').strip().lower()
        try:
            order = Order.objects.prefetch_related('items').get(
                order_number=order_number,
                shipping_email__iexact=email
            )
        except Order.DoesNotExist:
            messages.error(request, 'Order not found. Please check your details and try again.')
    return render(request, 'orders/tracking.html', {'order': order})
