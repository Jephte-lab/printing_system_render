# orders/models.py
from django.db import models
from clients.models import Client
from services.models import Service

class Order(models.Model):
    STATUS_CHOICES = (
        ('pending', 'Pending'),
        ('cleared', 'Cleared'),
    )

    client = models.ForeignKey(Client, on_delete=models.CASCADE)
    name = models.CharField(max_length=200, blank=True)
    status = models.CharField(max_length=10, choices=STATUS_CHOICES, default='pending')
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name or f"Order #{self.id}"

    @property
    def total_price(self):
        return sum(item.total_price for item in self.items.all())


class OrderItem(models.Model):
    order = models.ForeignKey(Order, related_name="items", on_delete=models.CASCADE)
    service = models.ForeignKey(Service, on_delete=models.PROTECT)
    quantity = models.PositiveIntegerField(default=1)
    unit_price = models.DecimalField(max_digits=10, decimal_places=2)
    total_price = models.DecimalField(max_digits=12, decimal_places=2, blank=True)

    def save(self, *args, **kwargs):
        self.total_price = self.unit_price * self.quantity
        super().save(*args, **kwargs)
