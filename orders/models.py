"""
Orders Models - Order, OrderItem, Payment
"""
from django.db import models
from django.conf import settings
from django.utils import timezone
import uuid

from store.models import Product, ProductVariant
from users.models import Address


class Order(models.Model):
    """Customer order"""
    STATUS_CHOICES = [
        ('pending', 'Pending'),
        ('confirmed', 'Confirmed'),
        ('processing', 'Processing'),
        ('shipped', 'Shipped'),
        ('out_for_delivery', 'Out for Delivery'),
        ('delivered', 'Delivered'),
        ('cancelled', 'Cancelled'),
        ('refunded', 'Refunded'),
    ]
    PAYMENT_STATUS = [
        ('unpaid', 'Unpaid'),
        ('paid', 'Paid'),
        ('failed', 'Failed'),
        ('refunded', 'Refunded'),
    ]
    PAYMENT_METHOD = [
        ('stripe', 'Credit/Debit Card'),
        ('paypal', 'PayPal'),
        ('cod', 'Cash on Delivery'),
    ]

    id = models.UUIDField(primary_key=True, default=uuid.uuid4, editable=False)
    order_number = models.CharField(max_length=20, unique=True, blank=True)
    user = models.ForeignKey(
        settings.AUTH_USER_MODEL, on_delete=models.SET_NULL,
        null=True, blank=True, related_name='orders'
    )

    # Address snapshot
    shipping_name = models.CharField(max_length=200)
    shipping_email = models.EmailField()
    shipping_phone = models.CharField(max_length=20)
    shipping_address = models.TextField()
    shipping_city = models.CharField(max_length=100)
    shipping_state = models.CharField(max_length=100)
    shipping_postal = models.CharField(max_length=20)
    shipping_country = models.CharField(max_length=100, default='United States')

    # Pricing
    subtotal = models.DecimalField(max_digits=10, decimal_places=2)
    discount_amount = models.DecimalField(max_digits=10, decimal_places=2, default=0)
    shipping_cost = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    tax_amount = models.DecimalField(max_digits=8, decimal_places=2, default=0)
    total_price = models.DecimalField(max_digits=10, decimal_places=2)

    # Status
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='pending')
    payment_status = models.CharField(max_length=20, choices=PAYMENT_STATUS, default='unpaid')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD, default='stripe')

    # Payment refs
    stripe_payment_intent = models.CharField(max_length=200, blank=True)
    paypal_order_id = models.CharField(max_length=200, blank=True)

    # Coupon
    coupon_code = models.CharField(max_length=50, blank=True)

    # Tracking
    tracking_number = models.CharField(max_length=100, blank=True)
    notes = models.TextField(blank=True)

    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    delivered_at = models.DateTimeField(null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def save(self, *args, **kwargs):
        if not self.order_number:
            self.order_number = f'LM{timezone.now().strftime("%Y%m%d")}{str(uuid.uuid4())[:6].upper()}'
        super().save(*args, **kwargs)

    def __str__(self):
        return f'Order #{self.order_number}'

    @property
    def tracking_steps(self):
        steps = ['pending', 'confirmed', 'processing', 'shipped', 'out_for_delivery', 'delivered']
        current_index = steps.index(self.status) if self.status in steps else 0
        return [(step, i <= current_index) for i, step in enumerate(steps)]


class OrderItem(models.Model):
    """Individual items in an order"""
    order = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, null=True)
    product_name = models.CharField(max_length=300)  # Snapshot
    product_image = models.CharField(max_length=500, blank=True)  # Snapshot
    variant_info = models.CharField(max_length=200, blank=True)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.quantity}x {self.product_name}"

    @property
    def total_price(self):
        return self.unit_price * self.quantity
