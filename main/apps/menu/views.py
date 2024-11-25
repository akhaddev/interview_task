from rest_framework import generics 
from .serializer import MenuCreateSerializer, MenuListSerializer
from ..common.pagination import CustomPagination
from rest_framework import permissions
from rest_framework_simplejwt import authentication
from rest_framework.response import Response
from rest_framework import status
from .models import Menu
from io import BytesIO
from django.core.files.base import ContentFile
import qrcode
from .models import MenuQrCode
from rest_framework.decorators import api_view



class MenuCreateAPIView(generics.CreateAPIView):
    serializer_class = MenuCreateSerializer
    authentication_classes = [authentication.JWTAuthentication]
    permission_classes = [permissions.IsAuthenticated]

    def create(self, request, *args, **kwargs):
        serializer = self.get_serializer(data=request.data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_201_CREATED)

menu_create_api_view = MenuCreateAPIView.as_view()



class MenuListAPIView(generics.ListAPIView):
    serializer_class = MenuListSerializer
    pagination_class = CustomPagination

    def get_queryset(self):
        queryset = Menu.objects.all()
        name = self.request.query_params.get('name', None)
        tags = self.request.query_params.get('tags', None)

        if name:
            queryset = queryset.filter(name__icontains=name)

        if tags:
            queryset = queryset.filter(tags__icontains=tags)
        return queryset

menu_list_api_view = MenuListAPIView.as_view()



class MenuDetailView(generics.RetrieveUpdateDestroyAPIView):
    queryset = Menu.objects.all()
    # authentication_classes = [authentication.JWTAuthentication]
    # permission_classes = [permissions.IsAuthenticated]
    lookup_field='guid'

    def get_serializer_class(self):
        if self.request.method == 'PUT' or 'PATCH':
            return MenuCreateSerializer
        else:
            return MenuListSerializer

menu_retrieve_update_delete_api_view = MenuDetailView.as_view()



@api_view(['GET'])
def generate_qr_code(request):
    menu_list_url = request.build_absolute_uri('/api/v1/menu/list/')
    print('menu_list_url', menu_list_url)

    qr = qrcode.make(menu_list_url)
    buffer = BytesIO()
    qr.save(buffer, format="PNG")
    buffer.seek(0)

    qr_code_instance = MenuQrCode()
    qr_code_instance.qr_code.save("menu_list_qr.png", ContentFile(buffer.getvalue()))
    qr_code_instance.save()

    qr_code_url = request.build_absolute_uri(qr_code_instance.qr_code.url)

    return Response({
        "message": "QR code generated and saved successfully.",
        "qr_code_url": qr_code_url,
    })

qrcode_generate_api_view = generate_qr_code




