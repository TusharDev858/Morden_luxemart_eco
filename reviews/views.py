from django.shortcuts import redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse
from .models import Review
from store.models import Product


@login_required
def add_review(request, product_id):
    if request.method == 'POST':
        product = get_object_or_404(Product, pk=product_id)
        existing = Review.objects.filter(product=product, user=request.user).first()
        if existing:
            messages.warning(request, 'You have already reviewed this product.')
            return redirect('store:product_detail', slug=product.slug)

        rating = int(request.POST.get('rating', 5))
        title = request.POST.get('title', '').strip()
        body = request.POST.get('body', '').strip()

        if not body:
            messages.error(request, 'Review body is required.')
            return redirect('store:product_detail', slug=product.slug)

        Review.objects.create(
            product=product, user=request.user,
            rating=rating, title=title, body=body
        )
        messages.success(request, 'Thank you for your review!')
    return redirect('store:product_detail', slug=product.slug)
