from django.db import models

class Service(models.Model):
    name = models.CharField(max_length=100)   # Plate Cards, Dance Floor, etc.
    base_price = models.DecimalField(max_digits=10, decimal_places=2)
    description = models.TextField(blank=True)

    def __str__(self):
        return self.name
