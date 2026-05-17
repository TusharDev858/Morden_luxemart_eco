"""
Cart Models - Session-based shopping cart
"""
from django.db import models
from django.conf import settings
from store.models import Product, ProductVariant


class Cart(models.Model):
    """Shopping cart - tied to session or user"""
    user = models.OneToOneField(
        settings.AUTH_USER_MODEL, on_delete=models.CASCADE,
        null=True, blank=True, related_name='cart'
    )
    session_key = models.CharField(max_length=40, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    coupon_code = models.CharField(max_length=50, blank=True)
    coupon_discount = models.DecimalField(max_digits=8, decimal_places=2, default=0)

    def __str__(self):
        return f"Cart - {self.user or self.session_key}"

    @property
    def total_items(self):
        return sum(item.quantity for item in self.items.all())

    @property
    def subtotal(self):
        return sum(item.total_price for item in self.items.all())

    @property
    def total(self):
        return max(self.subtotal - self.coupon_discount, 0)


class CartItem(models.Model):
    """Individual cart item"""
    cart = models.ForeignKey(Cart, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    variant = models.ForeignKey(ProductVariant, on_delete=models.SET_NULL, null=True, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    added_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.quantity}x {self.product.name}"

    @property
    def unit_price(self):
        base_price = self.product.current_price
        if self.variant:
            base_price += self.variant.price_modifier
        return base_price

    @property
    def total_price(self):
        return self.unit_price * self.quantity
