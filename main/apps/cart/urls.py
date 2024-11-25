from django.urls import path
from . import views


urlpatterns = [
    path(
        "create/", 
        views.cart_create_api_view,
        name='cart_create'
    ),
    path(
        "list/", 
        views.cart_list_api_view, 
        name="cart_list"
    ),
    path(
        "update/<uuid:guid>/", 
        views.cart_update_api_view, 
        name="cart_update"
    ),
    path(
        "delete/<uuid:guid>/", 
        views.cart_delete_api_view, 
        name="cart_delete"
    ),
]


