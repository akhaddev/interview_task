from rest_framework import serializers 
from .models import Order, OrderItem



class OrderSerializer(serializers.ModelSerializer):
    class Meta:
        model = Order
        fields = (
            'id',
            'guid',
            'menu_items',
            'total_price'
        )



class OrderItemSerializer(serializers.ModelSerializer):
    class Meta:
        model = OrderItem
        fields = (
            'id',
            'guid',
            'order',
            'menu_item',
            'quantity'
        )

