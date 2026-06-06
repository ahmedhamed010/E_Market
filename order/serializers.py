from rest_framework import serializers

from .models import *


class OrderItemsSerializer(serializers.ModelSerializer):
    class Meta :
        model = OrderItem
        fields = '__all__'


class OrderSerializer(serializers.ModelSerializer):
    orderItems = serializers.SerializerMethodField(method_name="get_order_items" , read_only=True)
    class Meta :
        model = Order
        fields = '__all__'
    def get_order_items(self , obj):
        order_items = obj.orderitems.all()
        serializer = OrderItemsSerializer(order_items , many=True)
        return serializer.data


class CartItemSerializer(serializers.ModelSerializer):
    product_name = serializers.CharField(
        source='product.name',
        read_only=True
    )

    product_price = serializers.DecimalField(
        source='product.price',
        max_digits=7,
        decimal_places=2,
        read_only=True
    )
    class Meta:
        model = CartItem
        fields = '__all__'


class CartSerializer(serializers.ModelSerializer):
    cart_items = CartItemSerializer(many=True , read_only=True)
    class Meta:
        model = Cart
        fields = '__all__'