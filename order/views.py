from django.shortcuts import render , get_object_or_404 
from rest_framework.response import Response
from rest_framework import viewsets , status , mixins
from rest_framework.permissions import IsAuthenticated , IsAdminUser
from rest_framework.decorators import permission_classes , api_view

from .models import Order , OrderItem
from .serializers import OrderSerializer
from products.models import Product

# Create your views here.


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_all_orders(request):
    orders = Order.objects.all()
    serializer = OrderSerializer(orders , many=True)
    return Response({'Orders':serializer.data})



@api_view(['GET'])
@permission_classes([IsAuthenticated])
def get_order(request,pk):
    order = get_object_or_404(Order , id=pk)
    serializer = OrderSerializer(order)
    return Response({'Order':serializer.data})



@api_view(['PUT'])
@permission_classes([IsAuthenticated , IsAdminUser])
def update_order(request , pk):
    order = get_object_or_404(Order , id=pk)
    order.status = request.data['status']
    order.payment_status = request.data['payment_status']
    order.payment_mode = request.data['payment_mode']
    order.save()
    serializer = OrderSerializer(order)
    return Response({'success':serializer.data})



@api_view(['DELETE'])
@permission_classes([IsAuthenticated])
def delete_order(request , pk):
    order = get_object_or_404(Order , id=pk)
    order.delete()
    return Response({'success':"Order Deleted Is Successfully"})



@api_view(['POST'])
@permission_classes([IsAuthenticated])
def new_order(request):
    user = request.user
    data = request.data
    order_items = data['order_items']
    
    if order_items and len(order_items) == 0 :
        return Response({'error':'No Order Recieved'} , status=status.HTTP_400_BAD_REQUEST)
    else :
        total_amount = sum(item['price']*item['quantity'] for item in order_items)
        order = Order.objects.create(
            user = user ,
            city = data['city'] ,
            zip_code = data['zip_code'] ,
            street = data['street'] ,
            phone_number = data['phone_number'] ,
            country = data['country'] , 
            total_amount = total_amount ,
        )
        for i in order_items :
            product = Product.objects.get(id=i['product'])
            item = OrderItem.objects.create(
                product = product,
                order = order ,
                name = product.name ,
                quantity = i['quantity'] ,
                price = i['price']
            )
            product.stock -= item.quantity
            product.save()
        serializer = OrderSerializer(order , many=False)
        return Response(serializer.data)
