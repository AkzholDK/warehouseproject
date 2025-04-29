from django.contrib import admin
from .models import Category, Product, Supply, SupplyItem, Shipment, ShipmentItem, Notification

admin.site.register(Category)
admin.site.register(Product)
admin.site.register(Supply)
admin.site.register(SupplyItem)
admin.site.register(Shipment)
admin.site.register(ShipmentItem)
admin.site.register(Notification)
