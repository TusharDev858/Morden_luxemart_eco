def wishlist_context(request):
    if request.user.is_authenticated:
        wishlist_ids = list(request.user.wishlist_items.values_list('product_id', flat=True))
        return {'wishlist_ids': wishlist_ids, 'wishlist_count': len(wishlist_ids)}
    return {'wishlist_ids': [], 'wishlist_count': 0}
