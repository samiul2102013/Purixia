from django.db import models
from django.conf import settings
from apps.catalog.models import Product


class DeliveryType(models.TextChoices):
    INSIDE  = 'inside',  'Inside Dhaka'
    OUTSIDE = 'outside', 'Outside Dhaka'


class PaymentMethod(models.TextChoices):
    COD    = 'cod',   'Cash on Delivery'
    CARD   = 'card',  'Card'
    BKASH  = 'bkash', 'bKash'
    NAGAD  = 'nagad', 'Nagad'


class OrderStatus(models.TextChoices):
    PENDING   = 'pending',   'Pending'
    CONFIRMED = 'confirmed', 'Confirmed'
    SHIPPED   = 'shipped',   'Shipped'
    DELIVERED = 'delivered', 'Delivered'
    CANCELLED = 'cancelled', 'Cancelled'


class ShippingInfo(models.Model):
    name    = models.CharField(max_length=200)
    email   = models.EmailField()
    phone   = models.CharField(max_length=20)
    address = models.TextField()

    def __str__(self):
        return f'{self.name} — {self.phone}'


class Order(models.Model):
    user           = models.ForeignKey(settings.AUTH_USER_MODEL, on_delete=models.CASCADE, related_name='orders')
    shipping_info  = models.OneToOneField(ShippingInfo, on_delete=models.PROTECT)
    delivery_type  = models.CharField(max_length=20, choices=DeliveryType.choices, default=DeliveryType.INSIDE)
    payment_method = models.CharField(max_length=20, choices=PaymentMethod.choices, default=PaymentMethod.COD)
    status         = models.CharField(max_length=20, choices=OrderStatus.choices, default=OrderStatus.PENDING)
    total_amount   = models.DecimalField(max_digits=12, decimal_places=2, default=0)
    created_at     = models.DateTimeField(auto_now_add=True)
    updated_at     = models.DateTimeField(auto_now=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f'Order #{self.id} — {self.user}'


class OrderItem(models.Model):
    order      = models.ForeignKey(Order, on_delete=models.CASCADE, related_name='items')
    product    = models.ForeignKey(Product, on_delete=models.PROTECT)
    quantity   = models.PositiveIntegerField()
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)

    @property
    def subtotal(self):
        if self.unit_price is not None and self.quantity is not None:
            return self.unit_price * self.quantity
        return 0

    def __str__(self):
        return f'{self.quantity}x {self.product.name}'