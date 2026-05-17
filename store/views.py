"""
Store Views - Homepage, Product Catalog, Product Detail, Search
"""
from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView
from django.db.models import Q, Avg
from django.http import JsonResponse
from django.contrib import messages
from django.core.paginator import Paginator

from .models import Product, Category, Banner, Brand, Coupon
from reviews.models import Review


def home(request):
    """Homepage with all sections"""
    banners = Banner.objects.filter(is_active=True)[:5]
    featured_products = Product.objects.filter(
        is_active=True, is_featured=True
    ).prefetch_related('gallery')[:8]
    trending_products = Product.objects.filter(
        is_active=True, is_trending=True
    ).prefetch_related('gallery')[:8]
    new_arrivals = Product.objects.filter(
        is_active=True, is_new_arrival=True
    ).prefetch_related('gallery')[:8]
    categories = Category.objects.filter(is_active=True, parent=None).order_by('order')[:8]
    best_sellers = Product.objects.filter(
        is_active=True, is_best_seller=True
    ).prefetch_related('gallery')[:4]
    testimonials = Review.objects.filter(
        is_approved=True
    ).select_related('user', 'product').order_by('-created_at')[:6]

    return render(request, 'store/home.html', {
        'banners': banners,
        'featured_products': featured_products,
        'trending_products': trending_products,
        'new_arrivals': new_arrivals,
        'categories': categories,
        'best_sellers': best_sellers,
        'testimonials': testimonials,
    })


class ProductListView(ListView):
    """Product catalog with filtering, search, sorting"""
    model = Product
    template_name = 'store/product_list.html'
    context_object_name = 'products'
    paginate_by = 12

    def get_queryset(self):
        queryset = Product.objects.filter(is_active=True).prefetch_related('gallery').select_related('category', 'brand')
        # Category filter from URL
        category_slug = self.kwargs.get('slug')
        if category_slug:
            self.category = get_object_or_404(Category, slug=category_slug, is_active=True)
            queryset = queryset.filter(category=self.category)
        else:
            self.category = None
            # Category from GET param
            cat_slug = self.request.GET.get('category')
            if cat_slug:
                try:
                    cat = Category.objects.get(slug=cat_slug)
                    queryset = queryset.filter(category=cat)
                except Category.DoesNotExist:
                    pass

        # Search
        q = self.request.GET.get('q', '').strip()
        if q:
            queryset = queryset.filter(
                Q(name__icontains=q) | Q(description__icontains=q) |
                Q(category__name__icontains=q) | Q(brand__name__icontains=q)
            )

        # Brand
        brand = self.request.GET.get('brand', '').strip()
        if brand:
            queryset = queryset.filter(brand__slug=brand)

        # Price range
        try:
            min_price = self.request.GET.get('min_price')
            if min_price:
                queryset = queryset.filter(price__gte=float(min_price))
            max_price = self.request.GET.get('max_price')
            if max_price:
                queryset = queryset.filter(price__lte=float(max_price))
        except (ValueError, TypeError):
            pass

        # Type filter
        filter_type = self.request.GET.get('filter', '')
        filter_map = {
            'featured': {'is_featured': True},
            'trending': {'is_trending': True},
            'new': {'is_new_arrival': True},
            'sale': {'discount_price__isnull': False},
            'best_seller': {'is_best_seller': True},
        }
        if filter_type in filter_map:
            queryset = queryset.filter(**filter_map[filter_type])

        # Sorting
        sort_map = {
            'price_asc': 'price', 'price_desc': '-price',
            'name_asc': 'name', 'name_desc': '-name',
            'newest': '-created_at', 'oldest': 'created_at',
        }
        sort = self.request.GET.get('sort', 'newest')
        queryset = queryset.order_by(sort_map.get(sort, '-created_at'))
        return queryset

    def get_context_data(self, **kwargs):
        ctx = super().get_context_data(**kwargs)
        ctx['category'] = getattr(self, 'category', None)
        ctx['categories'] = Category.objects.filter(is_active=True, parent=None).order_by('order')
        ctx['brands'] = Brand.objects.filter(is_active=True)
        ctx['search_query'] = self.request.GET.get('q', '')
        ctx['current_sort'] = self.request.GET.get('sort', 'newest')
        ctx['selected_brand'] = self.request.GET.get('brand', '')
        ctx['min_price'] = self.request.GET.get('min_price', '')
        ctx['max_price'] = self.request.GET.get('max_price', '')
        ctx['filter_options'] = [
            ('All Products', ''), ('Featured', 'featured'),
            ('Trending 🔥', 'trending'), ('New Arrivals', 'new'),
            ('On Sale', 'sale'), ('Best Sellers', 'best_seller'),
        ]
        return ctx


def product_detail(request, slug):
    """Full product detail page"""
    product = get_object_or_404(Product, slug=slug, is_active=True)
    images = product.gallery.all()
    variants = product.variants.all()
    reviews = product.reviews.filter(is_approved=True).select_related('user').order_by('-created_at')
    related_products = Product.objects.filter(
        category=product.category, is_active=True
    ).exclude(pk=product.pk).prefetch_related('gallery')[:4]
    user_reviewed = False
    if request.user.is_authenticated:
        user_reviewed = reviews.filter(user=request.user).exists()
    return render(request, 'store/product_detail.html', {
        'product': product,
        'images': images,
        'variants': variants,
        'reviews': reviews,
        'related_products': related_products,
        'user_reviewed': user_reviewed,
    })


def search(request):
    """Search results page"""
    query = request.GET.get('q', '').strip()
    products = Product.objects.none()
    if query:
        products = Product.objects.filter(is_active=True).filter(
            Q(name__icontains=query) | Q(description__icontains=query) |
            Q(category__name__icontains=query) | Q(brand__name__icontains=query)
        ).prefetch_related('gallery').select_related('category')
    paginator = Paginator(products, 12)
    page_obj = paginator.get_page(request.GET.get('page'))
    return render(request, 'store/search.html', {
        'products': page_obj,
        'query': query,
        'total': paginator.count,
    })


def validate_coupon(request):
    """AJAX coupon validation"""
    if request.method == 'POST':
        code = request.POST.get('code', '').strip().upper()
        try:
            coupon = Coupon.objects.get(code=code)
            if coupon.is_valid():
                suffix = '%' if coupon.discount_type == 'percentage' else ''
                prefix = '' if coupon.discount_type == 'percentage' else '$'
                return JsonResponse({
                    'valid': True,
                    'discount_type': coupon.discount_type,
                    'discount_value': str(coupon.discount_value),
                    'message': f'Coupon applied! {prefix}{coupon.discount_value}{suffix} off your order 🎉'
                })
            return JsonResponse({'valid': False, 'message': 'This coupon has expired or is no longer valid.'})
        except Coupon.DoesNotExist:
            return JsonResponse({'valid': False, 'message': 'Invalid coupon code. Please check and try again.'})
    return JsonResponse({'error': 'Invalid request'}, status=400)
