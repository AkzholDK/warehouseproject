from django.db import models
from django.contrib.auth.models import User

class Category(models.Model):
    name = models.CharField(max_length=100)

    def __str__(self):
        return self.name

class Product(models.Model):
    name = models.CharField(max_length=100)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True, blank=True)
    price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.PositiveIntegerField(default=0)
    min_quantity = models.PositiveIntegerField(default=0)
    image = models.ImageField(upload_to='product_images/', null=True, blank=True)

    def __str__(self):
        return self.name

class Supply(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    supplier = models.CharField(max_length=100)
    created_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='supplies', null=True)

    def __str__(self):
        return f"Supply from {self.supplier} — {self.date.date()}"

class SupplyItem(models.Model):
    supply = models.ForeignKey(Supply, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

class Shipment(models.Model):
    date = models.DateTimeField(auto_now_add=True)
    client = models.CharField(max_length=100)
    client_address = models.CharField(max_length=255, null=True, blank=True)
    client_phone = models.CharField(max_length=15, null=True, blank=True)
    client_email = models.EmailField(null=True, blank=True)
    payment_status = models.CharField(max_length=50, choices=[('paid', 'Paid'), ('pending', 'Pending')], default='pending')
    delivery_date = models.DateField(null=True, blank=True)
    shipping_method = models.CharField(max_length=50, choices=[('standard', 'Standard'), ('express', 'Express')], default='standard')

    def __str__(self):
        return f"Shipment for {self.client}"

class ShipmentItem(models.Model):
    shipment = models.ForeignKey(Shipment, related_name='items', on_delete=models.CASCADE)
    product = models.ForeignKey(Product, on_delete=models.CASCADE)
    quantity = models.PositiveIntegerField()

    def __str__(self):
        return f"{self.product.name} - {self.quantity}"

class Notification(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name="notifications")
    message = models.CharField(max_length=255)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.message} ({'Read' if self.is_read else 'New'})"
