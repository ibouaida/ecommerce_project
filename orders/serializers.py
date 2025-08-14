from rest_framework import serializers
from .models import Order, OrderItem
from products.serializers import ProductSerializer

class OrderItemSerializer(serializers.ModelSerializer):
    product = ProductSerializer(read_only=True)
    
    class Meta:
        model = OrderItem
        fields = ['id', 'product', 'quantity', 'price', 'total']

class OrderSerializer(serializers.ModelSerializer):
    items = OrderItemSerializer(many=True, read_only=True)
    
    class Meta:
        model = Order
        fields = ['id', 'customer_name', 'customer_email', 'customer_phone', 
                 'customer_address', 'total_amount', 'status', 'created_at', 'items']
        read_only_fields = ['id', 'status', 'created_at', 'items']

class CreateOrderSerializer(serializers.ModelSerializer):
    items_data = serializers.ListField(
        child=serializers.DictField(),
        write_only=True
    )
    
    class Meta:
        model = Order
        fields = ['customer_name', 'customer_email', 'customer_phone', 
                 'customer_address', 'total_amount', 'items_data']
    
    def validate_customer_phone(self, value):
        """Validation optionnelle du numéro de téléphone"""
        if value and len(value.strip()) == 0:
            return None
        return value
    
    def create(self, validated_data):
        items_data = validated_data.pop('items_data')
        order = Order.objects.create(**validated_data)
        
        for item_data in items_data:
            OrderItem.objects.create(
                order=order,
                product_id=item_data['product_id'],
                quantity=item_data['quantity'],
                price=item_data['price']
            )
        
        return order 