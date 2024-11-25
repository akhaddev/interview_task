from main.apps.cart.models import Cart
from rest_framework import generics 
from .models import Order, OrderItem
from .serializer import (
    OrderSerializer,
    OrderItemSerializer
)
from ..common.pagination import CustomPagination
from rest_framework import permissions
from rest_framework_simplejwt import authentication

from rest_framework import generics, status
from rest_framework.response import Response
from .utils import send_order_to_telegram
from asgiref.sync import async_to_sync



class OrderCreateAPIView(generics.CreateAPIView):
    serializer_class = OrderSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        cart_items = Cart.objects.filter(user=user)

        if not cart_items.exists():
            return Response({'error': 'Your cart is empty'}, status=status.HTTP_400_BAD_REQUEST)

        total_price = sum(item.menu_item.price * item.quantity for item in cart_items)
        order = Order.objects.create(user=user, total_price=total_price)

        order_items = []
        for cart_item in cart_items:
            order_item = OrderItem(
                order=order,
                menu_item=cart_item.menu_item,
                quantity=cart_item.quantity
            )
            order_items.append(order_item)

        OrderItem.objects.bulk_create(order_items)
        cart_items.delete()

        order_items_data = [
            {"menu_item_name": item.menu_item.name, "quantity": item.quantity}
            for item in order_items
        ]
        async_to_sync(send_order_to_telegram)(order.user.username, order_items_data, total_price)

        return Response({'message': 'Order placed successfully!'}, status=status.HTTP_201_CREATED)


order_create_api_view = OrderCreateAPIView.as_view()



class OrderListView(generics.ListAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]    
    pagination_class = CustomPagination

order_list_api_view = OrderListView.as_view()



class OrderDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Order.objects.all()
    serializer_class = OrderSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]  
    lookup_field='guid'  

order_retrieve_update_delete_api_view = OrderDetailView.as_view()


