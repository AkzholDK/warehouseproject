from rest_framework import serializers
from .models import Product, Supply, SupplyItem, Shipment, ShipmentItem, Category

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['id', 'name']

class ProductSerializer(serializers.ModelSerializer):
    category = CategorySerializer(read_only=True)

    class Meta:
        model = Product
        fields = '__all__'

class SupplyItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = SupplyItem
        fields = '__all__'

class SupplySerializer(serializers.ModelSerializer):
    items = SupplyItemSerializer(many=True, read_only=True)

    class Meta:
        model = Supply
        fields = '__all__'

class ShipmentItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)

    class Meta:
        model = ShipmentItem
        fields = '__all__'

class ShipmentSerializer(serializers.ModelSerializer):
    items = ShipmentItemSerializer(many=True, read_only=True)

    class Meta:
        model = Shipment
        fields = '__all__'
