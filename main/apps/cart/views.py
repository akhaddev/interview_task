from rest_framework import generics 
from .serializer import CartSerializer
from ..common.pagination import CustomPagination
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework import status
from .models import Cart
from ..menu.models import Menu
from django.db.models import Q



class CartCreateAPIView(generics.CreateAPIView):
    serializer_class = CartSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        user = request.user
        menu_item_id = request.data.get('menu_item')
        quantity = request.data.get('quantity', 1)

        try:
            menu_item = Menu.objects.get(id=menu_item_id)
        except Menu.DoesNotExist:
            return Response({'error': 'Menu item not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item, created = Cart.objects.get_or_create(user=user, menu_item=menu_item)
        if not created:
            cart_item.quantity += int(quantity)  
        else:
            cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_201_CREATED)

cart_create_api_view = CartCreateAPIView.as_view()



class CartListAPIView(generics.ListAPIView):
    serializer_class = CartSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user.id)

cart_list_api_view = CartListAPIView.as_view()



class CartUpdateAPIView(generics.UpdateAPIView):
    serializer_class = CartSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

    def update(self, request, *args, **kwargs):
        cart_item_id = kwargs.get('pk')  
        quantity = request.data.get('quantity')

        try:
            cart_item = self.get_queryset().get(id=cart_item_id)
        except Cart.DoesNotExist:
            return Response({'error': 'Cart item not found'}, status=status.HTTP_404_NOT_FOUND)

        cart_item.quantity = int(quantity)
        cart_item.save()

        serializer = self.get_serializer(cart_item)
        return Response(serializer.data, status=status.HTTP_200_OK)

cart_update_api_view = CartUpdateAPIView.as_view()



class CartDeleteAPIView(generics.DestroyAPIView):
    serializer_class = CartSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        return Cart.objects.filter(user=self.request.user)

cart_delete_api_view = CartDeleteAPIView.as_view()




