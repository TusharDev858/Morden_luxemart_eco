"""
Users Views - Auth, Profile, Dashboard, Addresses
"""
from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth import login, logout, authenticate, update_session_auth_hash
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from django.http import JsonResponse

from .models import CustomUser, Address, NewsletterSubscriber
from .forms import UserRegistrationForm, UserLoginForm, UserProfileForm, AddressForm
from orders.models import Order


def register(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == 'POST':
        form = UserRegistrationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user, backend='django.contrib.auth.backends.ModelBackend')
            messages.success(request, f'Welcome to LuxeMart, {user.first_name or user.username}! Your account is ready.')
            return redirect('store:home')
    else:
        form = UserRegistrationForm()
    return render(request, 'users/register.html', {'form': form})


def user_login(request):
    if request.user.is_authenticated:
        return redirect('store:home')
    if request.method == 'POST':
        form = UserLoginForm(request, data=request.POST)
        if form.is_valid():
            email = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(request, username=email, password=password)
            if user:
                login(request, user)
                messages.success(request, f'Welcome back, {user.first_name or user.email}!')
                next_url = request.GET.get('next', '')
                return redirect(next_url) if next_url else redirect('store:home')
        messages.error(request, 'Invalid email or password. Please try again.')
    else:
        form = UserLoginForm()
    return render(request, 'users/login.html', {'form': form})


def user_logout(request):
    logout(request)
    messages.info(request, 'You have been logged out. See you soon!')
    return redirect('store:home')


@login_required
def profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            messages.success(request, 'Profile updated successfully!')
            return redirect('users:profile')
    else:
        form = UserProfileForm(instance=request.user)
    addresses = request.user.addresses.all()
    recent_orders = Order.objects.filter(user=request.user).order_by('-created_at')[:5]
    return render(request, 'users/profile.html', {
        'form': form, 'addresses': addresses, 'recent_orders': recent_orders,
    })


@login_required
def dashboard(request):
    orders = Order.objects.filter(user=request.user).order_by('-created_at')
    wishlist_count = request.user.wishlist_items.count()
    total_spent = sum(o.total_price for o in orders if o.payment_status == 'paid')
    return render(request, 'users/dashboard.html', {
        'orders': orders[:10],
        'total_orders': orders.count(),
        'wishlist_count': wishlist_count,
        'total_spent': total_spent,
    })


@login_required
def add_address(request):
    if request.method == 'POST':
        form = AddressForm(request.POST)
        if form.is_valid():
            addr = form.save(commit=False)
            addr.user = request.user
            addr.save()
            messages.success(request, 'Address added successfully!')
            return redirect('users:profile')
    else:
        form = AddressForm()
    return render(request, 'users/address_form.html', {'form': form, 'title': 'Add New Address'})


@login_required
def edit_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    if request.method == 'POST':
        form = AddressForm(request.POST, instance=address)
        if form.is_valid():
            form.save()
            messages.success(request, 'Address updated successfully!')
            return redirect('users:profile')
    else:
        form = AddressForm(instance=address)
    return render(request, 'users/address_form.html', {'form': form, 'title': 'Edit Address'})


@login_required
def delete_address(request, pk):
    address = get_object_or_404(Address, pk=pk, user=request.user)
    address.delete()
    messages.success(request, 'Address removed.')
    return redirect('users:profile')


def newsletter_subscribe(request):
    if request.method == 'POST':
        email = request.POST.get('email', '').strip().lower()
        if email and '@' in email:
            sub, created = NewsletterSubscriber.objects.get_or_create(email=email)
            if created:
                if request.user.is_authenticated:
                    request.user.newsletter_subscribed = True
                    request.user.save(update_fields=['newsletter_subscribed'])
                return JsonResponse({'success': True, 'message': "You're subscribed! Check your inbox for a welcome gift 🎁"})
            return JsonResponse({'success': False, 'message': 'This email is already subscribed.'})
        return JsonResponse({'success': False, 'message': 'Please enter a valid email address.'})
    return JsonResponse({'success': False, 'message': 'Invalid request'}, status=400)
