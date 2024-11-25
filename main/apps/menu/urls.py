from django.urls import path
from . import views


urlpatterns = [
    path(
        "create/", 
        views.menu_create_api_view,
        name='menu_create'
    ),
    path(
        "list/", 
        views.menu_list_api_view, 
        name="menu_list"
    ),
    path(
        "detail/<uuid:guid>/", 
        views.menu_retrieve_update_delete_api_view, 
        name="menu_detail"
    ),

    path(
        "qrcode-generate/", 
        views.qrcode_generate_api_view, 
        name="qrcode_generate"
    ),
]


